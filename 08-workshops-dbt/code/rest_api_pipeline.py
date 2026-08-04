from __future__ import annotations

import argparse

import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_source


BASE_URL = "https://test-agent-traces-api-xt2e7ottma-ew.a.run.app"


def build_source(
    base_url: str = BASE_URL,
    page_size: int = 1000,
    maximum_offset: int | None = 0,
    incremental: bool = False,
):
    # The records are inside the API response under the "logs" key.
    resource = {
        "name": "logs",
        "endpoint": {
            "path": "/logs",
            "data_selector": "logs",
        },
        "primary_key": "index",
    }

    if incremental:
        resource["incremental"] = dlt.sources.incremental("index")

    paginator = {
        "type": "offset",
        "limit": page_size,
        "offset": 0,
        "limit_param": "limit",
        "offset_param": "offset",
        "total_path": "total",
    }

    if maximum_offset is not None:
        paginator["maximum_offset"] = maximum_offset

    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "paginator": paginator,
        },
        "resources": [resource],
    }

    return rest_api_source(
        config,
        name="agent_traces",
        max_table_nesting=2,
    )


def run_pipeline(
    destination: str = "duckdb",
    dataset_name: str = "agent_logs",
    page_size: int = 1000,
    maximum_offset: int | None = 0,
    write_disposition: str = "replace",
    dev_mode: bool = True,
    incremental: bool = False,
):
    source = build_source(
        page_size=page_size,
        maximum_offset=maximum_offset,
        incremental=incremental,
    )

    pipeline = dlt.pipeline(
        pipeline_name="agent_traces",
        destination=destination,
        dataset_name=dataset_name,
        dev_mode=dev_mode,
    )

    load_info = pipeline.run(source, write_disposition=write_disposition)
    print(load_info)
    return load_info


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load hosted fake Claude Code traces with dlt REST API source."
    )
    parser.add_argument("--full", action="store_true", help="Load all available API pages.")
    parser.add_argument("--destination", default="duckdb", choices=["duckdb", "playground"])
    parser.add_argument("--dataset-name", default="agent_logs")
    parser.add_argument("--page-size", type=int, default=1000)
    parser.add_argument(
        "--maximum-offset",
        type=int,
        default=None,
        help="Override the offset cap. Sample mode defaults to 0 for one page.",
    )
    parser.add_argument("--write-disposition", default="replace")
    parser.add_argument("--merge", action="store_true", help="Use merge loading.")
    parser.add_argument("--incremental", action="store_true", help="Use index as a cursor.")
    parser.add_argument("--no-dev-mode", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    maximum_offset = args.maximum_offset
    if maximum_offset is None:
        maximum_offset = None if args.full else 0

    write_disposition = "merge" if args.merge else args.write_disposition

    run_pipeline(
        destination=args.destination,
        dataset_name=args.dataset_name,
        page_size=args.page_size,
        maximum_offset=maximum_offset,
        write_disposition=write_disposition,
        dev_mode=not args.no_dev_mode,
        incremental=args.incremental,
    )
