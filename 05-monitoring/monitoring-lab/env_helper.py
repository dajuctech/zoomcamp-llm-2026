from pathlib import Path

from dotenv import load_dotenv


def load_course_env():
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        env_path = parent / ".env"

        if env_path.exists():
            load_dotenv(env_path)
            return env_path

    return None
