import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fitness_assistant.db import get_db_connection


def print_rows(title, rows):
    print(f"\n{title}")
    print("-" * len(title))

    if not rows:
        print("No rows found")
        return

    for row in rows:
        print(row)


def main():
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM conversations")
            conversations_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM feedback")
            feedback_count = cur.fetchone()[0]

            print("Database summary")
            print("----------------")
            print(f"Conversations: {conversations_count}")
            print(f"Feedback: {feedback_count}")

            cur.execute(
                """
                SELECT
                    id,
                    question,
                    relevance,
                    ROUND(openai_cost::numeric, 6),
                    timestamp
                FROM conversations
                ORDER BY timestamp DESC
                LIMIT 5
                """
            )
            print_rows("Latest conversations", cur.fetchall())

            cur.execute(
                """
                SELECT
                    id,
                    conversation_id,
                    feedback,
                    timestamp
                FROM feedback
                ORDER BY timestamp DESC
                LIMIT 5
                """
            )
            print_rows("Latest feedback", cur.fetchall())

    finally:
        conn.close()


if __name__ == "__main__":
    main()
