"""요청 기록용 SQLite 로거 (조회량 모니터링, 논리적 요청 단위)."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent.parent / "state" / "request_log.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS request_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    tag TEXT,
    kind TEXT NOT NULL,
    detail TEXT,
    status TEXT NOT NULL DEFAULT 'ok'
);
"""


@contextmanager
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def log_request(tag: str, kind: str, detail: Optional[str] = None, status: str = "ok") -> None:
    """kind: 'hashtag_listing' | 'post_detail'"""
    with _connect() as conn:
        conn.execute(
            "INSERT INTO request_log (ts, tag, kind, detail, status) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), tag, kind, detail, status),
        )
