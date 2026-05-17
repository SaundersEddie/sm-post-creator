from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from models import FactItem


TONE_INSTRUCTIONS = {
    "simple": "Use a clear, simple, friendly tone.",
    "witty": "Use a conversational tone with light wit. Do not be smug or mean.",
    "nostalgic": "Use a warm, reflective, nostalgic tone.",
    "educational": "Use an informative but still conversational tone.",
    "engagement": "Use a conversational tone and end with a simple engagement question.",
    "snarky-lite": "Use mild playful sarcasm, but do not insult people or the subject.",
}


def _build_prompt(fact: FactItem, tone: str) -> str:
    tone_instruction = TONE_INSTRUCTIONS.get(
        tone,
        TONE_INSTRUCTIONS["witty"],
    )

    return f"""
Write a Facebook post using only the factual data below.

Rules:
- Do not add extra facts.
- Do not invent dates, names, quotes, awards, chart positions, relationships, or causes.
- Keep the post between 60 and 120 words.
- {tone_instruction}
- You MUST include a final line labeled exactly: Hashtags:
- The Hashtags line MUST contain 4 to 7 relevant hashtags.
- Each hashtag must start with #.
- Include the source link on a separate line labeled exactly: Source:
- Plain text only.
- Do not use markdown headings.

Factual data:
Category: {fact.category}
Title: {fact.title}
Date: {fact.date_label}
Year: {fact.year}
Fact: {fact.fact}
Source name: {fact.source_name}
Source URL: {fact.source_url}
""".strip()


def generate_post(fact: FactItem, tone: str = "witty") -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to your .env file."
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=_build_prompt(fact, tone),
    )

    return response.output_text.strip()
