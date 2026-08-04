from __future__ import annotations

import sys
from pathlib import Path

from dlt.hub import run
from dlt.hub.run import trigger


PROJECT_DIR = Path(__file__).resolve().parent
CODE_DIR = PROJECT_DIR / "code"

if str(CODE_DIR) not in sys.path:
    sys.path.append(str(CODE_DIR))

from agent_traces_dashboard import app as agent_traces_dashboard
from rest_api_pipeline import run_pipeline


@run.pipeline("agent_traces", trigger=trigger.schedule("0 12 * * *"))
def ingest_agent_logs():
    return run_pipeline(
        destination="playground",
        dataset_name="agent_logs",
        page_size=1000,
        maximum_offset=0,
        write_disposition="replace",
        dev_mode=False,
    )


__all__ = ["ingest_agent_logs", "agent_traces_dashboard"]
