from __future__ import annotations

import argparse
from pathlib import Path

import dlt
from dlt.sources.filesystem import filesystem, read_jsonl


DEFAULT_LOG_DIR = "~/.claude/projects"


def resolve_bucket_url(bucket_url: str) -> str:
    if "://" in bucket_url:
        return bucket_url

    return str(Path(bucket_url).expanduser())


def local_jsonl_files_exist(bucket_url: str) -> bool:
    if "://" in bucket_url:
        return True

    path = Path(bucket_url).expanduser()
    return path.exists() and any(path.rglob("*.jsonl"))


def build_reader(bucket_url: str, file_glob: str, max_table_nesting: int):
    # The workshop starts with local JSONL logs and lets dlt parse each JSON line.
    reader = (
        filesystem(bucket_url=bucket_url, file_glob=file_glob)
        | read_jsonl()
    ).with_name("messages")

    # Keeping nesting lower reduces schema pollution from deeply nested agent logs.
    reader.apply_hints(max_table_nesting=max_table_nesting)

    return reader


def run_pipeline(
    bucket_url: str = DEFAULT_LOG_DIR,
    file_glob: str = "**/*.jsonl",
    max_table_nesting: int = 1,
    write_disposition: str = "replace",
    dev_mode: bool = True,
):
    bucket_url = resolve_bucket_url(bucket_url)

    if not local_jsonl_files_exist(bucket_url):
        raise SystemExit(
            "No JSONL logs found. Pass a folder with --bucket-url, "
            "for example --bucket-url ~/.claude/projects"
        )

    reader = build_reader(
        bucket_url=bucket_url,
        file_glob=file_glob,
        max_table_nesting=max_table_nesting,
    )

    pipeline = dlt.pipeline(
        pipeline_name="agent_logs",
        destination="duckdb",
        dataset_name="agent_logs",
        dev_mode=dev_mode,
    )

    load_info = pipeline.run(reader, write_disposition=write_disposition)
    print(load_info)
    return load_info


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load local coding-agent JSONL logs into DuckDB with dlt."
    )
    parser.add_argument("--bucket-url", default=DEFAULT_LOG_DIR)
    parser.add_argument("--file-glob", default="**/*.jsonl")
    parser.add_argument("--max-table-nesting", type=int, default=1)
    parser.add_argument("--write-disposition", default="replace")
    parser.add_argument("--no-dev-mode", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    run_pipeline(
        bucket_url=args.bucket_url,
        file_glob=args.file_glob,
        max_table_nesting=args.max_table_nesting,
        write_disposition=args.write_disposition,
        dev_mode=not args.no_dev_mode,
    )
