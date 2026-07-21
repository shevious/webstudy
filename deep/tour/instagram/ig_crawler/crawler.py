"""해시태그 기준 게시물 수집: 개수 상한 + 증분 수집(last_seen)."""
import itertools
import time
from pathlib import Path
from typing import Any, Dict, List

import instaloader

from . import db, downloader, state

DEFAULT_LIMIT = 5
REQUEST_DELAY_SEC = 2  # 게시물 상세 조회 사이 지연 (차단 위험 완화용)


def crawl_hashtag(
    loader: instaloader.Instaloader,
    tag: str,
    data_dir: Path,
    limit: int = DEFAULT_LIMIT,
) -> List[Dict[str, Any]]:
    """해시태그 게시물을 최대 limit개, 이전 실행 이후 신규분만 data_dir/tag/<post_id>/ 에 저장한다."""
    hashtag = instaloader.Hashtag.from_name(loader.context, tag)
    db.log_request(tag, "hashtag_listing", detail=f"limit={limit}")
    last_seen = state.get_last_seen(tag)

    new_posts = []
    for post in itertools.islice(hashtag.get_posts_resumable(), limit):
        if last_seen is not None and post.mediaid == last_seen:
            break
        new_posts.append(post)

    if not new_posts:
        print(f"[{tag}] 신규 게시물 없음")
        return []

    downloaded = []
    for post in new_posts:
        post_dir = data_dir / tag / str(post.mediaid)
        try:
            result = downloader.download_post(loader, post.mediaid, post_dir)
        except Exception as exc:
            db.log_request(tag, "post_detail", detail=str(post.mediaid), status="error")
            print(f"  ! {post.mediaid} 실패: {type(exc).__name__}: {exc}")
            continue
        db.log_request(tag, "post_detail", detail=str(post.mediaid), status="ok")
        downloaded.append(result)
        print(f"  + {post.mediaid} 미디어 {result['media_count']}개 / 파일 {result['file_count']}개")
        time.sleep(REQUEST_DELAY_SEC)

    state.set_last_seen(tag, new_posts[0].mediaid)
    print(f"[{tag}] {len(downloaded)}개 게시물 수집 완료 -> {data_dir / tag}")
    return downloaded
