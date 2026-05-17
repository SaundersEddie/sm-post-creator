import os
from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()

APP_USER_AGENT = os.getenv(
    "APP_USER_AGENT",
    "FactPostGenerator/0.1 (contact@example.com)"
).strip()

OUTPUT_PATH = "output/posts.txt"
