import argparse
import json
import os

import requests


def post_json(url, payload):
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Send a test question to the Flask API.")
    parser.add_argument(
        "question",
        nargs="?",
        default="What exercise can I do for chest?",
    )
    parser.add_argument(
        "--url",
        default=os.getenv("APP_URL", "http://localhost:5001"),
    )
    parser.add_argument(
        "--feedback",
        type=int,
        choices=[1, -1],
        default=None,
    )

    args = parser.parse_args()
    base_url = args.url.rstrip("/")

    answer = post_json(
        f"{base_url}/question",
        {"question": args.question},
    )

    print(json.dumps(answer, indent=2))

    if args.feedback is not None:
        feedback = post_json(
            f"{base_url}/feedback",
            {
                "conversation_id": answer["conversation_id"],
                "feedback": args.feedback,
            },
        )

        print(json.dumps(feedback, indent=2))


if __name__ == "__main__":
    main()
