from pathlib import Path

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


COURSE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(COURSE_ROOT / ".env")


provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
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
answer = rag.rag(query)

print(answer)
