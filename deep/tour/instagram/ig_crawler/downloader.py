"""게시물 상세 조회 및 미디어 저장.

instaloader의 download_post()는 인스타그램이 거부하는 GraphQL doc_id를 사용해 동작하지 않으므로,
동작이 확인된 iPhone API(api/v1/media/{id}/info/)를 직접 호출한다.
"""
import json
from pathlib import Path
from typing import Optional

import instaloader

MEDIA_TYPE_IMAGE = 1
MEDIA_TYPE_VIDEO = 2
MEDIA_TYPE_CAROUSEL = 8


def _best_image_url(media: dict) -> Optional[str]:
    candidates = media.get("image_versions2", {}).get("candidates") or []
    return candidates[0]["url"] if candidates else None


def _best_video_url(media: dict) -> Optional[str]:
    versions = media.get("video_versions") or []
    return versions[0]["url"] if versions else None


def _download_file(context: instaloader.InstaloaderContext, url: str, dest: Path) -> None:
    with context.get_anonymous_session() as session:
        resp = session.get(url, stream=True)
        resp.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 16):
                fh.write(chunk)


def _save_media(context: instaloader.InstaloaderContext, media: dict, dest_dir: Path, index: int) -> int:
    """단일 미디어(이미지 또는 동영상)를 저장하고 저장한 파일 수를 반환한다."""
    saved = 0
    video_url = _best_video_url(media)
    if video_url:
        _download_file(context, video_url, dest_dir / f"{index}.mp4")
        saved += 1

    image_url = _best_image_url(media)
    if image_url:
        # 동영상이면 썸네일로 함께 저장한다.
        suffix = "_thumb" if video_url else ""
        _download_file(context, image_url, dest_dir / f"{index}{suffix}.jpg")
        saved += 1

    return saved


def download_post(loader: instaloader.Instaloader, mediaid: int, dest_dir: Path) -> dict:
    """게시물의 캡션·메타데이터·이미지·동영상을 dest_dir에 저장한다."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    item = loader.context.get_iphone_json(f"api/v1/media/{mediaid}/info/", {})["items"][0]

    caption = (item.get("caption") or {}).get("text", "")
    (dest_dir / "caption.txt").write_text(caption, encoding="utf-8")
    (dest_dir / "metadata.json").write_text(
        json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    media_list = item.get("carousel_media") or [item]
    file_count = sum(
        _save_media(loader.context, media, dest_dir, i) for i, media in enumerate(media_list)
    )

    return {
        "mediaid": mediaid,
        "shortcode": item.get("code"),
        "media_count": len(media_list),
        "file_count": file_count,
        "caption_len": len(caption),
    }
