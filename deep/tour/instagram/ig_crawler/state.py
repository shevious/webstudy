"""해시태그별 마지막으로 수집한 게시물 ID 저장/로드 (증분 수집용)."""
import json
from pathlib import Path
from typing import Optional

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
STATE_FILE = STATE_DIR / "last_seen.json"


def _load_all() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def get_last_seen(tag: str) -> Optional[int]:
    return _load_all().get(tag)


def set_last_seen(tag: str, mediaid: int) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    data = _load_all()
    data[tag] = mediaid
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
