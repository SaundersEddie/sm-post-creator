from dataclasses import dataclass


@dataclass
class FactItem:
    category: str
    title: str
    date_label: str
    year: int | None
    fact: str
    source_url: str
    source_name: str = "Wikipedia"
    