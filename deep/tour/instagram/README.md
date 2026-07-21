# Instagram 해시태그 크롤러

특정 해시태그의 최신 게시물에서 **본문 텍스트 / 이미지 / 동영상**을 수집한다.

- 1회 실행당 수집 개수 상한(기본 5개)
- 증분 수집: 이전 실행에서 본 게시물을 만나면 중단
- 요청량을 SQLite에 기록해 과도한 조회 여부를 추적

---

## 1. 사전 준비

### 1.1 환경

| 항목 | 이 문서에서 검증한 값 |
|---|---|
| OS | Ubuntu (Linux 6.2) |
| Python | 3.14.4 |
| 패키지 관리 | uv 0.11.28 (venv 생성), pip 26.1.2 (패키지 설치) |
| 브라우저 | Firefox (snap 설치본) |

Python 3.9 이상이면 동작한다. Firefox는 **로그인 쿠키를 가져오기 위해 필수**다(3.2 참고).

### 1.2 인스타그램 계정

- 로그인 없이는 해시태그 조회가 불가능하므로 **계정이 반드시 필요**하다.
- 자동화로 인한 제재 위험이 있으므로 **본계정 대신 서브/테스트 계정**을 권장한다.
- 계정에 2단계 인증(2FA)이 걸려 있어도 무방하다(브라우저에서 로그인하므로).

---

## 2. 설치

```bash
mkdir -p ~/workspace/instagram && cd ~/workspace/instagram

# venv 생성 (uv 사용. python -m venv 로 대체 가능)
uv venv

# uv venv는 pip을 포함하지 않으므로 별도 설치
uv pip install pip

# 의존성 설치
.venv/bin/pip install instaloader browser_cookie3
```

`requirements.txt`로 한 번에 설치해도 된다.

```
instaloader>=4.15
browser_cookie3>=0.19
```

```bash
.venv/bin/pip install -r requirements.txt
```

**검증한 버전**: instaloader 4.15.2, browser-cookie3 0.20.1

---

## 3. 로그인 방식과 그 이유 (중요)

### 3.1 아이디/비밀번호 로그인이 실패하는 이유

`instaloader.Instaloader.login(user, passwd)`를 직접 호출하면 다음 순서로 막힌다.

1. **`LoginException: Checkpoint required`**
   인스타그램이 "의심스러운 로그인"으로 판단해 브라우저 인증을 요구한다.
   메시지에 나오는 `/auth_platform/?apc=...` 경로 앞에 `https://www.instagram.com`을 붙여
   **로그아웃 상태의 브라우저**에서 열고 인증을 완료해야 한다.
   (이미 로그인된 브라우저에서 열면 기존 쿠키로 통과해버려 스크립트 세션이 검증되지 않는다.)

2. 인증을 마쳐도 이번엔 **`403 Forbidden / login_required`** 가 발생한다.
   API 로그인으로 만들어진 세션에는 브라우저가 자연스럽게 갖는 `mid`, `rur` 쿠키가 없어서
   iPhone 계열 엔드포인트(`i.instagram.com`)가 세션을 인정하지 않는다.

### 3.2 채택한 방식: Firefox 쿠키 임포트

**같은 기기의 Firefox**에 로그인된 인스타그램 세션 쿠키를 그대로 읽어 쓴다.
`sessionid`, `csrftoken`, `mid`, `rur`, `ds_user_id` 등 8개 쿠키가 모두 넘어오므로 위 문제가 해결된다.

절차:

1. Firefox에서 인스타그램에 **정상 로그인**해 둔다(피드가 보이는 상태).
2. 스크립트를 실행하면 자동으로 쿠키를 읽어 로그인하고,
   `state/sessions/session-<username>` 에 세션을 저장한다.
3. 이후 실행은 저장된 세션 파일을 재사용한다(브라우저·비밀번호 불필요).

> **snap Firefox 경로 주의**
> snap으로 설치된 Firefox는 `~/.mozilla`가 아니라
> `~/snap/firefox/common/.mozilla/firefox/<프로필>/cookies.sqlite` 를 사용한다.
> `browser_cookie3`의 기본 탐색 경로로는 찾지 못하므로 `auth.py`에서 이 경로를 직접 지정한다.
> 일반(apt/deb) 설치본이라면 해당 glob이 비어 `None`이 반환되고 기본 탐색으로 넘어간다.

쿠키가 정상적으로 읽히는지 단독 확인:

```bash
.venv/bin/python -c "
import browser_cookie3
from pathlib import Path
root = Path.home()/'snap'/'firefox'/'common'/'.mozilla'/'firefox'
m = list(root.glob('*/cookies.sqlite'))
cs = list(browser_cookie3.firefox(cookie_file=str(m[0]) if m else None, domain_name='instagram.com'))
print(len(cs), [c.name for c in cs])
"
```

`sessionid`가 목록에 있어야 한다.

---

## 4. 프로젝트 구조

```
instagram/
├── main.py                 # CLI 진입점
├── requirements.txt
├── .gitignore              # .venv/ data/ state/ 제외
├── ig_crawler/
│   ├── __init__.py
│   ├── auth.py             # 세션 재사용 → Firefox 쿠키 → 대화형 로그인
│   ├── crawler.py          # 해시태그 조회, 개수 상한, 증분 수집
│   ├── downloader.py       # 게시물 상세 조회 및 미디어 저장
│   ├── state.py            # last_seen.json 읽기/쓰기
│   └── db.py               # 요청 로그 SQLite 기록
├── data/                   # 수집 결과 (git 제외)
└── state/                  # 세션·상태·로그 (git 제외)
    ├── sessions/session-<username>
    ├── last_seen.json
    └── request_log.db
```

---

## 5. 구현상 알아야 할 함정

instaloader 4.15.2 기준으로 **라이브러리 기본 API 두 개가 인스타그램 변경으로 동작하지 않는다.**
아래 우회가 이 프로젝트의 핵심이다.

### 5.1 `Hashtag.get_posts()` → `get_posts_resumable()`

`get_posts()`는 응답에서 `edge_hashtag_to_media`를 찾다 실패하면
`SectionIterator`로 폴백하는데, 현재 응답에는 `more_available` 키가 없어 `KeyError`로 죽는다.

```
KeyError: 'more_available'
```

**해결**: `get_posts_resumable()`을 사용한다. GraphQL 기반이며 정상 동작한다.
(instaloader 문서도 `get_posts()`를 deprecated로 표시하고 이쪽을 권장한다.)

### 5.2 `Instaloader.download_post()` → iPhone API 직접 호출

`download_post()`는 내부적으로 `Post._obtain_metadata()`를 호출하고,
이때 쓰이는 GraphQL doc_id(`8845758582119845`)를 인스타그램이 거부한다.

```
BadResponseException: Fetching Post metadata failed.
```

실제 응답:

```json
{"errors": [{"message": "execution error", "severity": "CRITICAL"}], "data": null, "status": "ok"}
```

**해결**: 동작이 확인된 iPhone 엔드포인트를 직접 호출한다.

```python
item = loader.context.get_iphone_json(f"api/v1/media/{mediaid}/info/", {})["items"][0]
```

이 응답에는 필요한 모든 것이 들어 있다.

| 필요한 것 | 위치 |
|---|---|
| 본문 텍스트 | `item["caption"]["text"]` |
| 여러 장/영상 묶음 | `item["carousel_media"]` (없으면 `item` 자신이 단일 미디어) |
| 이미지 URL | `media["image_versions2"]["candidates"][0]["url"]` (첫 번째가 최고 화질) |
| 동영상 URL | `media["video_versions"][0]["url"]` |

`media_type`: 1=이미지, 2=동영상, 8=캐러셀.
다만 실제 판별은 `video_versions` 존재 여부로 하는 편이 안전하다.

---

## 6. 사용법

```bash
cd ~/workspace/instagram
.venv/bin/python main.py --tag "영종도여행" --username <계정ID>
```

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--tag` | 해시태그 (`#` 제외) | 필수 |
| `--username` | 세션 파일 이름에 쓰이는 계정 식별자 | 필수 |
| `--limit` | 1회 최대 수집 개수 | 5 |

### 실행 예시

```
Loaded session from /home/.../state/sessions/session-<username>.
  + 3945142874781382453 미디어 2개 / 파일 2개
  + 3945043826982211691 미디어 5개 / 파일 5개
  + 3944811934710215727 미디어 5개 / 파일 5개
  + 3944767385374472590 미디어 1개 / 파일 1개
  + 3944747504453666398 미디어 20개 / 파일 26개
[영종도여행] 5개 게시물 수집 완료 -> /home/.../data/영종도여행
```

곧바로 재실행하면 증분 수집이 동작한다.

```
[영종도여행] 신규 게시물 없음
```

### 저장 구조

```
data/<태그>/<게시물ID>/
├── caption.txt        # 본문 텍스트
├── metadata.json      # API 원본 응답 전체
├── 0.jpg, 1.jpg …     # 이미지 (캐러셀은 순번대로)
└── 6.mp4, 6_thumb.jpg # 동영상 + 썸네일
```

---

## 7. 수집량 관리

### 7.1 개수 상한 + 증분 수집

두 조건 중 **먼저 걸리는 쪽**에서 멈춘다.

1. `--limit` 개수에 도달
2. `state/last_seen.json`에 기록된 게시물 ID를 만남 (해시태그 피드는 최신순)

`get_posts_resumable()`은 게으른 이터레이터라, `islice`로 자르면 그 이상은 **요청 자체가 나가지 않는다.**

### 7.2 요청 로그 확인

논리적 요청 단위로 `state/request_log.db`(SQLite)에 기록한다.

```sql
CREATE TABLE request_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,      -- UTC ISO8601
    tag TEXT,
    kind TEXT NOT NULL,    -- 'hashtag_listing' | 'post_detail'
    detail TEXT,           -- limit=5 / 게시물ID
    status TEXT NOT NULL   -- 'ok' | 'error'
);
```

```bash
# 전체 로그
sqlite3 state/request_log.db "SELECT ts, tag, kind, detail, status FROM request_log ORDER BY id;"

# 일자별 사용량
sqlite3 state/request_log.db "SELECT date(ts), kind, COUNT(*) FROM request_log GROUP BY 1,2;"
```

> `sqlite3` CLI가 없으면 `.venv/bin/python -c "import sqlite3; ..."` 로 대체할 수 있다.

### 7.3 차단을 피하려면

- 게시물 상세 조회 사이에 **2초 지연**을 둔다 (`crawler.py`의 `REQUEST_DELAY_SEC`).
- `--limit`을 크게 잡을수록 요청은 목록 조회보다 **상세 조회 쪽에서** 빠르게 늘어난다
  (목록 1회 + 게시물 수만큼 상세 조회).
- 처음에는 5개 정도로 시작해 로그를 보며 늘리는 것을 권장한다.

---

## 8. 문제 해결

| 증상 | 원인과 대처 |
|---|---|
| `Checkpoint required` | 3.1 참고. 로그아웃 상태 브라우저에서 인증 URL 접속 후 완료. 이후에는 Firefox 쿠키 방식이 우회해준다. |
| `403 / login_required` | Firefox에서 인스타그램 로그인이 풀렸을 가능성. 재로그인 후 `state/sessions/` 의 세션 파일을 지우고 다시 실행. |
| `404 Not Found` (태그 조회) | **해당 해시태그가 실제로 존재하지 않는다.** 앱/웹 검색창에서 정확한 표기를 확인할 것. (예: `ヨンジョンド旅行`은 존재하지 않고 `영종도여행`은 존재) |
| `KeyError: 'more_available'` | `get_posts()`를 쓰고 있다. `get_posts_resumable()`로 교체 (5.1). |
| `BadResponseException: Fetching Post metadata failed.` | `download_post()`를 쓰고 있다. iPhone API 직접 호출로 교체 (5.2). |
| 쿠키를 못 읽음 | Firefox가 실행 중이면 `cookies.sqlite`가 잠길 수 있다. 종료 후 재시도. snap 경로도 확인 (3.2). |
| 받은 mp4가 Totem에서 재생 안 됨 | 파일 문제가 아니라 H.264 디코더 부재. Firefox에 끌어다 놓으면 재생된다. 시스템 전체에서 재생하려면 `sudo apt install gstreamer1.0-libav gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly`. |

파일 자체가 정상인지 확인:

```bash
ffprobe -v error -show_entries stream=codec_name,profile,width,height \
  -of default=noprint_wrappers=1 data/<태그>/<ID>/6.mp4
# codec_name=h264 / profile=High 등이 나오면 정상
```

---

## 9. 제약과 주의사항

- **비공개 계정**의 게시물은 수집되지 않는다.
- 해시태그의 `mediacount`에는 접근 불가능한 게시물도 포함되므로, 실제 수집 가능 수와 다르다.
- instaloader는 인스타그램의 비공개 API에 의존하므로, **인스타그램 변경으로 언제든 깨질 수 있다.**
  5절의 두 우회도 같은 성격이며, 깨질 경우 응답 JSON을 직접 확인해 대응해야 한다.
- 해시태그 여러 개를 AND로 검색하는 기능은 인스타그램에 없다.
  여러 태그가 필요하면 각각 조회한 뒤 애플리케이션에서 합집합/교집합을 계산해야 한다.
- 자동 수집은 인스타그램 이용약관과 충돌할 수 있고, 계정 제재로 이어질 수 있다.
  수집 대상과 용도, 개인정보 처리 여부를 스스로 확인할 것.
- `state/sessions/` 의 세션 파일은 **로그인 자격증명과 동등**하다. 공유·커밋 금지(`.gitignore`에 포함됨).
