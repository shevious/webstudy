"""인스타그램 로그인 및 세션 캐싱."""
import getpass
from pathlib import Path
from typing import Optional

import browser_cookie3
import instaloader

SESSION_DIR = Path(__file__).resolve().parent.parent / "state" / "sessions"

# snap으로 설치된 Firefox는 ~/.mozilla가 아닌 별도 경로를 쓴다.
FIREFOX_SNAP_PROFILE_ROOT = Path.home() / "snap" / "firefox" / "common" / ".mozilla" / "firefox"


def _session_path(username: str) -> Path:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    return SESSION_DIR / f"session-{username}"


def _find_firefox_cookie_file() -> Optional[str]:
    """snap Firefox 프로필의 cookies.sqlite 경로를 찾는다. 못 찾으면 None(기본 경로 탐색에 맡김)."""
    matches = list(FIREFOX_SNAP_PROFILE_ROOT.glob("*/cookies.sqlite"))
    return str(matches[0]) if matches else None


def _login_from_firefox_cookies(loader: instaloader.Instaloader) -> Optional[str]:
    """같은 기기의 Firefox에 로그인된 인스타그램 세션 쿠키를 그대로 가져온다."""
    try:
        cookies = {
            c.name: c.value
            for c in browser_cookie3.firefox(
                cookie_file=_find_firefox_cookie_file(), domain_name="instagram.com"
            )
        }
    except Exception:
        return None

    if not cookies:
        return None

    loader.context.update_cookies(cookies)
    return loader.test_login()


def get_loader(username: str) -> instaloader.Instaloader:
    """세션 파일 재사용 -> Firefox 쿠키 임포트 -> 대화형 로그인 순으로 시도한다."""
    loader = instaloader.Instaloader()
    session_file = _session_path(username)

    if session_file.exists():
        loader.load_session_from_file(username, str(session_file))
        return loader

    logged_in_user = _login_from_firefox_cookies(loader)
    if logged_in_user:
        loader.context.username = logged_in_user
        loader.save_session_to_file(str(session_file))
        print(f"Firefox 세션에서 로그인 정보를 가져왔습니다: {logged_in_user}")
        return loader

    password = getpass.getpass(f"{username}의 인스타그램 비밀번호: ")
    try:
        loader.login(username, password)
    except instaloader.TwoFactorAuthRequiredException:
        code = input("2단계 인증 코드: ").strip()
        loader.two_factor_login(code)

    loader.save_session_to_file(str(session_file))
    return loader
