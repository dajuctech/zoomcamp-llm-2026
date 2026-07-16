FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

RUN uv venv
RUN uv pip install \
    minsearch \
    openai \
    pandas \
    psycopg[binary] \
    pydantic \
    python-dotenv \
    requests \
    streamlit \
    tqdm

COPY 05-monitoring/monitoring-lab/ .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
