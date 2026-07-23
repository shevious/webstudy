# Isaac Sim 6.0 — pip 설치 & WebRTC 원격 스트리밍

Ubuntu 서버에 **Isaac Sim 6.0.1.0**을 pip로 설치하고, Mac 등 원격 클라이언트에서
**WebRTC**로 접속해 사용하기 위한 설정 모음입니다.

## 구성

| 파일 | 설명 |
|------|------|
| `install_isaacsim.sh` | Python 3.12 venv에 Isaac Sim 6.0 설치 |
| `run_stream.sh` | WebRTC 스트리밍 서버(헤드리스) 기동 |
| `venv/` | Python 3.12 가상환경 (Isaac Sim 설치 위치) |
| `stream.log` | 스트리밍 서버 실행 로그 |

## 요구 사항

- **Ubuntu 22.04**, GLIBC 2.35+
- **Python 3.12** — 최신 Isaac Sim(6.0.x)은 `==3.12.*` 요구
  (참고: 5.0=Python 3.11, 4.5=Python 3.10)
- **NVIDIA GPU** + 드라이버 (RTX 계열), 디스크 여유 ~20GB
- venv 경로: `<프로젝트 폴더>/venv` (`install_isaacsim.sh`가 참조하는 고정 경로)

## 1. venv 생성 (uv)

```bash
uv python install 3.12
uv venv --python 3.12 venv --python-preference only-managed --seed
```

- `--seed`: uv venv는 기본적으로 **pip를 넣지 않음** → `install_isaacsim.sh`가 `pip install`을 쓰므로 필수.
- `--python-preference only-managed`: **필수, 빠뜨리면 안 됨.**
  - Homebrew/Linuxbrew에 `python@3.12`가 설치돼 있으면 uv가 PATH에 없어도 고정 경로
    (`/home/linuxbrew/.linuxbrew/opt/python@3.12/...`)를 탐색해서 **그쪽을 우선 사용**해버림
    ([uv issue #9715](https://github.com/astral-sh/uv/issues/9715)).
  - Homebrew python은 자체 동적 링커(`/home/linuxbrew/.linuxbrew/lib/ld.so`)를 써서 시스템의
    `libGL.so.1` / `libcuda.so.1` / `libnvidia-ml.so.1`을 못 찾음 → Isaac Sim 기동 시
    `Vulkan 1.1 is not supported`, `Failed to create any GPU devices` 등으로 **GPU/스트리밍이 전부 죽음**.
  - `only-managed`를 주면 uv가 직접 받은 python-build-standalone 빌드(표준 `/lib64/ld-linux-x86-64.so.2` 사용)만
    쓰도록 강제해서 이 문제를 피함.
- 확인: `venv/pyvenv.cfg`의 `home =` 값이 `/home/linuxbrew/...`가 아니라
  `~/.local/share/uv/python/cpython-3.12-.../bin`이어야 정상.

## 2. 설치

```bash
./install_isaacsim.sh
```

- venv가 없으면 자동 생성(있으면 재사용), Python 3.12가 아니면 중단합니다.
- `isaacsim[all,extscache]==6.0.1.0`을 받습니다. **약 15GB 다운로드**로 시간이 걸립니다.
- 끝나면 `isaacsim import OK`가 출력됩니다.

## 3. 스트리밍 서버 기동

```bash
./run_stream.sh          # 포그라운드 (Ctrl+C 종료)
./run_stream.sh --bg     # 백그라운드, 로그는 stream.log
```

기본값(이 서버 기준):

| 항목 | 값 | 비고 |
|------|-----|------|
| `PUBLIC_IP` | `175.124.109.66` | 공인 IP (`sw112.iptime.org`) |
| `SIGNAL_PORT` | `49101` | WebRTC 시그널링 (TCP) |
| `STREAM_PORT` | `47999` | WebRTC 미디어 (UDP) |

값 변경은 환경변수로:

```bash
PUBLIC_IP=1.2.3.4 SIGNAL_PORT=49101 STREAM_PORT=47999 ./run_stream.sh
```

## 4. 공유기 포트포워딩 (원격 접속용)

WebRTC는 **외부 포트 = 내부 포트(1:1 동일)** 로 포워딩해야 합니다.
서버 내부 IP는 `192.168.2.74`.

| 프로토콜 | 외부 포트 | 내부 IP:포트 |
|----------|-----------|--------------|
| TCP (시그널) | 49101 | 192.168.2.74:49101 |
| UDP (미디어) | 47999 | 192.168.2.74:47999 |

> ⚠️ **TCP만 열면 안 됩니다.** UDP(미디어)가 막히면 연결은 되지만 **검은 화면**만 보입니다.

## 5. Mac 클라이언트 접속

1. NVIDIA **Isaac Sim WebRTC Streaming Client** 설치
   - Apple Silicon: `isaacsim-webrtc-streaming-client-2.0.0-macos-aarch64.dmg`
   - Intel: `...-macos-x86_64.dmg`
   - DMG 열어 앱을 **Applications**로 드래그
   - 첫 실행 시 Gatekeeper 차단되면:
     `xattr -dr com.apple.quarantine "/Applications/Isaac Sim WebRTC Streaming Client.app"`
2. 앱 실행 → **Server IP**: `PUBLIC_IP`로 설정한 값(`run_stream.sh` 참고, VPN 접속 시 사설 IP), 포트 `49101`
3. **Connect** → 뷰포트가 나타나면 성공

## 6. 기본 예제 실행 (Franka Pick Place)

GUI 접속 후 메뉴에서:

```
Window → Examples → Robotics Examples
  → (하단) Robotics Examples 탭 → MANIPULATION → Franka Pick Place
```

- 목록에서 **Load** → 씬 로드 완료 후 뷰포트의 ▶(Play) 버튼으로 시뮬레이션 시작.
- 같은 `MANIPULATION` 카테고리에 `Follow Target`, `Stacking` 등 다른 Franka 예제도 있음.
- (참고) `Window → Examples` 바로 아래 `Physics Examples`는 로봇과 무관한 순수 물리 데모라 Franka 없음.

## 트러블슈팅

| 증상 | 원인 / 해결 |
|------|-------------|
| **검은 화면** (연결은 됨) | `publicIp` 미설정 → 서버가 사설 IP를 광고. `run_stream.sh`가 `PUBLIC_IP`로 해결. UDP 미디어 포트 포워딩도 확인. |
| **연결 자체 실패** | 시그널 TCP(49101) 포워딩/방화벽 확인. 클라이언트 포트가 49101인지 확인. |
| 외부 포트 체커가 "닫힘"으로 표시 | 공유기가 **해외 IP를 차단** → check-host.net 등 해외 노드는 오탐. **국내 IP**에서 테스트. |
| 로그의 `ROS2 Bridge startup failed` | ROS 미설정 탓이며 **스트리밍과 무관**. 무시 가능. |
| 로그에 `libGL.so.1`/`libcuda.so.1`/`libnvidia-ml.so.1 cannot open shared object file`, `Vulkan 1.1 is not supported`, `Failed to create any GPU devices` | venv가 **Homebrew python**으로 만들어짐 (자체 링커라 시스템 GPU 라이브러리를 못 찾음). `venv/pyvenv.cfg`의 `home =` 확인 후, [1. venv 생성](#1-venv-생성-uv)대로 `--python-preference only-managed`로 venv 재생성 + `./install_isaacsim.sh` 재설치. |
| `install_isaacsim.sh` 실행 시 `No module named pip` | uv venv를 `--seed` 없이 만듦. `--seed` 옵션 추가해서 venv 재생성. |

### 상태 확인 명령

```bash
# 프로세스
pgrep -af isaacsim.exp.full.streaming
# 시그널 포트 리슨 여부
ss -tln | grep 49101
# 실시간 로그
tail -f stream.log
```

## 메모

- 첫 기동은 셰이더 컴파일/익스텐션 로딩으로 30~60초 걸립니다.
- 서버는 EULA 자동 동의(`OMNI_KIT_ACCEPT_EULA=YES`)로 실행됩니다.
