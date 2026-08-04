from __future__ import annotations

import marimo


app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import dlt
    import marimo as mo
    import pandas as pd

    return alt, dlt, mo, pd


@app.cell
def _(dlt, mo):
    mo.md("# Local Claude Logs Dashboard")

    pipeline = dlt.attach("agent_logs")
    dataset = pipeline.dataset()

    return dataset, pipeline


@app.cell
def _(dataset, pd):
    def query_df(sql: str):
        try:
            return dataset(sql).df()
        except Exception as exc:
            return pd.DataFrame({"error": [str(exc)]})

    return query_df,


@app.cell
def _(query_df):
    # This table name comes from .with_name("messages") in filesystem_pipeline.py.
    message_types = query_df(
        """
        SELECT
            COALESCE(type, 'unknown') AS message_type,
            COUNT(*) AS records
        FROM messages
        GROUP BY 1
        ORDER BY records DESC
        """
    )

    message_types
    return message_types,


@app.cell
def _(alt, message_types, mo):
    if "error" in message_types.columns:
        mo.md(f"Could not build message type chart: `{message_types['error'][0]}`")
    else:
        alt.Chart(message_types).mark_bar().encode(
            x=alt.X("message_type:N", sort="-y", title="Message type"),
            y=alt.Y("records:Q", title="Records"),
            tooltip=["message_type", "records"],
        ).properties(title="Messages by Type")


@app.cell
def _(query_df):
    model_usage = query_df(
        """
        SELECT
            COALESCE(message__model, model, 'unknown') AS model,
            COUNT(*) AS records
        FROM messages
        GROUP BY 1
        ORDER BY records DESC
        """
    )

    model_usage
    return model_usage,


@app.cell
def _(alt, mo, model_usage):
    if "error" in model_usage.columns:
        mo.md(f"Could not build model usage chart: `{model_usage['error'][0]}`")
    else:
        alt.Chart(model_usage).mark_bar().encode(
            x=alt.X("model:N", sort="-y", title="Model"),
            y=alt.Y("records:Q", title="Records"),
            tooltip=["model", "records"],
        ).properties(title="Model Usage")


@app.cell
def _(query_df):
    recent_messages = query_df(
        """
        SELECT *
        FROM messages
        LIMIT 20
        """
    )

    recent_messages
    return recent_messages,


@app.cell
def _(recent_messages):
    recent_messages


if __name__ == "__main__":
    app.run()
