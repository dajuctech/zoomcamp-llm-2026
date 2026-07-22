import sqlite3
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


COURSE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(COURSE_ROOT / ".env")


class SQLiteSpanExporter(SpanExporter):
    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
            """
        )
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self, timeout_millis=30000):
        self.conn.close()

    def force_flush(self, timeout_millis=30000):
        return True


provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")


from rag_helper import RAGBase
from starter import client, index


def calculate_cost(input_tokens, output_tokens):
    return (input_tokens * 0.05 + output_tokens * 0.40) / 1_000_000


class RAGTraced(RAGBase):
    def rag(self, query):
        with tracer.start_as_current_span("rag"):
            return super().rag(query)

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search"):
            return super().search(query, num_results=num_results)

    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            response = super().llm(prompt)

            usage = response.usage
            input_tokens = usage.input_tokens
            output_tokens = usage.output_tokens
            cost = calculate_cost(input_tokens, output_tokens)

            span.set_attribute("input_tokens", input_tokens)
            span.set_attribute("output_tokens", output_tokens)
            span.set_attribute("cost", cost)

            return response


query = "How does the agentic loop keep calling the model until it stops?"

rag = RAGTraced(index=index, llm_client=client)

for i in range(4):
    answer = rag.rag(query)
    print(answer)

trace.get_tracer_provider().force_flush()


conn = sqlite3.connect("traces.db")

df = pd.read_sql_query(
    """
    SELECT
        name,
        start_time,
        end_time,
        input_tokens,
        output_tokens,
        cost,
        (end_time - start_time) / 1000000.0 AS duration_ms
    FROM spans
    ORDER BY start_time
    """,
    conn,
)

print("\nSpan names:")
print(df["name"].drop_duplicates().tolist())

print("\nTotal duration by span name, excluding rag:")
print(
    df[df["name"] != "rag"]
    .groupby("name")["duration_ms"]
    .sum()
    .sort_values(ascending=False)
)

print("\nInput tokens for llm spans:")
print(df[df["name"] == "llm"]["input_tokens"].tolist())

conn.close()
