FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY 07-project-example/fitness-assistant/ ./

RUN uv pip install --system \
    flask \
    minsearch \
    openai \
    pandas \
    psycopg[binary] \
    python-dotenv

EXPOSE 5000

CMD ["python", "app.py"]
