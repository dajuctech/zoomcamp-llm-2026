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
    mo.md("# Agent Traces Dashboard")

    # Deployed notebooks must attach to the persistent playground destination.
    pipeline = dlt.attach(
        "agent_traces",
        destination="playground",
        dataset_name="agent_logs",
    )
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
    model_usage = query_df(
        """
        SELECT
            COALESCE(model, 'unknown') AS model,
            COUNT(*) AS records
        FROM logs
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
    token_usage = query_df(
        """
        SELECT
            COALESCE(model, 'unknown') AS model,
            SUM(COALESCE(usage__input_tokens, 0)) AS input_tokens,
            SUM(COALESCE(usage__output_tokens, 0)) AS output_tokens
        FROM logs
        GROUP BY 1
        ORDER BY input_tokens DESC
        """
    )

    token_usage
    return token_usage,


@app.cell
def _(alt, mo, token_usage):
    if "error" in token_usage.columns:
        mo.md(f"Could not build token chart: `{token_usage['error'][0]}`")
    else:
        chart_data = token_usage.melt(
            id_vars=["model"],
            value_vars=["input_tokens", "output_tokens"],
            var_name="token_type",
            value_name="tokens",
        )

        alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("model:N", title="Model"),
            y=alt.Y("tokens:Q", title="Tokens"),
            color="token_type:N",
            tooltip=["model", "token_type", "tokens"],
        ).properties(title="Token Usage by Model")


@app.cell
def _(query_df):
    recent_logs = query_df(
        """
        SELECT *
        FROM logs
        ORDER BY index DESC
        LIMIT 20
        """
    )

    recent_logs
    return recent_logs,


@app.cell
def _(recent_logs):
    recent_logs


if __name__ == "__main__":
    app.run()
