from datetime import datetime
from pathlib import Path

from models import FactItem


def export_posts(
    posts: list[tuple[FactItem, str]],
    output_path: str,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chunks: list[str] = []

    chunks.append(f"Generated posts")
    chunks.append(f"Generated at: {generated_at}")
    chunks.append("=" * 60)
    chunks.append("")

    for index, (fact, post_text) in enumerate(posts, start=1):
        chunks.append("=" * 60)
        chunks.append(f"POST #{index}")
        chunks.append(f"CATEGORY: {fact.category}")
        chunks.append(f"TITLE: {fact.title}")
        chunks.append(f"DATE: {fact.date_label}")
        chunks.append(f"YEAR: {fact.year}")
        chunks.append(f"SOURCE: {fact.source_url}")
        chunks.append("=" * 60)
        chunks.append("")
        chunks.append(post_text)
        chunks.append("")
        chunks.append("")

    path.write_text("\n".join(chunks), encoding="utf-8")
    
def export_raw_facts(
    facts: list,
    output_path: str,
    target_date,
    categories: list[str],
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chunks: list[str] = []

    chunks.append("RAW FACTS")
    chunks.append(f"Generated at: {generated_at}")
    chunks.append(f"Date: {target_date.isoformat()}")
    chunks.append(f"Categories: {', '.join(categories)}")
    chunks.append("=" * 60)
    chunks.append("")

    for index, fact in enumerate(facts, start=1):
        chunks.append("=" * 60)
        chunks.append(f"FACT #{index}")
        chunks.append(f"CATEGORY: {fact.category}")
        chunks.append(f"TITLE: {fact.title}")
        chunks.append(f"DATE: {fact.date_label}")
        chunks.append(f"YEAR: {fact.year}")
        chunks.append(f"SOURCE: {fact.source_url}")
        chunks.append("=" * 60)
        chunks.append("")
        chunks.append(fact.fact)
        chunks.append("")

    path.write_text("\n".join(chunks), encoding="utf-8")
    
    