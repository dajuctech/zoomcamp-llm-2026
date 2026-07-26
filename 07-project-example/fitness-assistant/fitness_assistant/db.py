import os
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import psycopg
from dotenv import load_dotenv


def find_course_root():
    current = Path(__file__).resolve()

    for path in [current, *current.parents]:
        if (path / "pyproject.toml").exists():
            return path

    return Path.cwd()


load_dotenv(find_course_root() / ".env")

TZ_INFO = os.getenv("TZ", "Europe/London")
tz = ZoneInfo(TZ_INFO)


def get_db_connection():
    last_error = None

    for _ in range(10):
        try:
            return psycopg.connect(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=os.getenv("POSTGRES_PORT", "5432"),
                dbname=os.getenv("POSTGRES_DB", "fitness_assistant"),
                user=os.getenv("POSTGRES_USER", "user"),
                password=os.getenv("POSTGRES_PASSWORD", "password"),
                connect_timeout=3,
            )
        except psycopg.OperationalError as error:
            last_error = error
            time.sleep(1)

    raise last_error


def init_db(drop=False):
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            if drop:
                cur.execute("DROP TABLE IF EXISTS feedback")
                cur.execute("DROP TABLE IF EXISTS conversations")

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    response_time FLOAT NOT NULL,
                    relevance TEXT NOT NULL,
                    relevance_explanation TEXT NOT NULL,
                    prompt_tokens INTEGER NOT NULL,
                    completion_tokens INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    eval_prompt_tokens INTEGER NOT NULL,
                    eval_completion_tokens INTEGER NOT NULL,
                    eval_total_tokens INTEGER NOT NULL,
                    openai_cost FLOAT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id SERIAL PRIMARY KEY,
                    conversation_id TEXT REFERENCES conversations(id),
                    feedback INTEGER NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """
            )

        conn.commit()

    finally:
        conn.close()


def save_conversation(conversation_id, question, answer_data, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)

    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversations (
                    id,
                    question,
                    answer,
                    model_used,
                    response_time,
                    relevance,
                    relevance_explanation,
                    prompt_tokens,
                    completion_tokens,
                    total_tokens,
                    eval_prompt_tokens,
                    eval_completion_tokens,
                    eval_total_tokens,
                    openai_cost,
                    timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    conversation_id,
                    question,
                    answer_data["answer"],
                    answer_data["model_used"],
                    answer_data["response_time"],
                    answer_data["relevance"],
                    answer_data["relevance_explanation"],
                    answer_data["prompt_tokens"],
                    answer_data["completion_tokens"],
                    answer_data["total_tokens"],
                    answer_data["eval_prompt_tokens"],
                    answer_data["eval_completion_tokens"],
                    answer_data["eval_total_tokens"],
                    answer_data["openai_cost"],
                    timestamp,
                ),
            )

        conn.commit()

    finally:
        conn.close()


def save_feedback(conversation_id, feedback, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)

    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO feedback (conversation_id, feedback, timestamp)
                VALUES (%s, %s, %s)
                """,
                (conversation_id, feedback, timestamp),
            )

        conn.commit()

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized")
