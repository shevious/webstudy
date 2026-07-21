"""인스타그램 해시태그 기준 게시물 수집기 CLI."""
import argparse
from pathlib import Path

from ig_crawler.auth import get_loader
from ig_crawler.crawler import DEFAULT_LIMIT, crawl_hashtag

DATA_DIR = Path(__file__).resolve().parent / "data"


def main():
    parser = argparse.ArgumentParser(description="인스타그램 해시태그 기준 게시물 수집기")
    parser.add_argument("--tag", required=True, help="검색할 해시태그 (# 제외)")
    parser.add_argument("--username", required=True, help="로그인에 사용할 인스타그램 계정")
    parser.add_argument(
        "--limit", type=int, default=DEFAULT_LIMIT, help=f"1회 최대 수집 개수 (기본 {DEFAULT_LIMIT})"
    )
    args = parser.parse_args()

    loader = get_loader(args.username)
    crawl_hashtag(loader, args.tag, DATA_DIR, limit=args.limit)


if __name__ == "__main__":
    main()
