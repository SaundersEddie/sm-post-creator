from datetime import datetime
from typing import Any

import requests

from config import APP_USER_AGENT
from models import FactItem


BASE_URL = "https://en.wikipedia.org/api/rest_v1/feed/onthisday"


def _get_page_url(item: dict[str, Any]) -> str:
    pages = item.get("pages", [])

    if not pages:
        return "https://en.wikipedia.org/"

    first_page = pages[0]
    content_urls = first_page.get("content_urls", {})
    desktop = content_urls.get("desktop", {})

    return desktop.get("page", "https://en.wikipedia.org/")


def _get_title(item: dict[str, Any]) -> str:
    pages = item.get("pages", [])

    if not pages:
        return "Untitled"

    first_page = pages[0]
    titles = first_page.get("titles", {})

    return (
        titles.get("normalized")
        or titles.get("display")
        or titles.get("canonical")
        or "Untitled"
    )


def fetch_on_this_day(
    event_type: str,
    month: int | None = None,
    day: int | None = None,
    limit: int = 5,
) -> list[FactItem]:
    """
    event_type examples:
    - selected
    - events
    - births
    - deaths
    - holidays
    - all
    """

    today = datetime.now()

    mm = f"{month or today.month:02d}"
    dd = f"{day or today.day:02d}"

    url = f"{BASE_URL}/{event_type}/{mm}/{dd}"

    headers = {
        "User-Agent": APP_USER_AGENT,
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    data = response.json()
    raw_items = data.get(event_type, [])

    facts: list[FactItem] = []

    for item in raw_items[:limit]:
        year = item.get("year")
        text = item.get("text", "").strip()

        if not text:
            continue

        title = _get_title(item)
        source_url = _get_page_url(item)

        facts.append(
            FactItem(
                category=event_type,
                title=title,
                date_label=f"{mm}/{dd}",
                year=year,
                fact=text,
                source_url=source_url,
                source_name="Wikipedia",
            )
        )

    return facts


def collect_default_facts(
    month: int | None = None,
    day: int | None = None,
    limit_per_category: int = 3,
    categories: list[str] | None = None,
) -> list[FactItem]:
    facts: list[FactItem] = []

    selected_categories = categories or [
        "selected",
        "events",
        "births",
    ]

    for category in selected_categories:
        facts.extend(
            fetch_on_this_day(
                event_type=category,
                month=month,
                day=day,
                limit=limit_per_category,
            )
        )

    return facts

