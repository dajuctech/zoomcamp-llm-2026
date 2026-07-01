from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH)

client = OpenAI()
MODEL = "gpt-5.4-mini"