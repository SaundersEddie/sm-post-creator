import random
import argparse
from datetime import datetime, date, timedelta

from ai_writer import generate_post
from post_exporter import export_posts, export_raw_facts
from wikimedia_collector import collect_default_facts


VALID_CATEGORIES = [
    "selected",
    "events",
    "births",
    "deaths",
    "holidays",
    "all",
]

DEFAULT_CATEGORIES = [
    "selected",
    "events",
    "births",
]

VALID_TONES = [
    "simple",
    "witty",
    "nostalgic",
    "educational",
    "engagement",
    "snarky-lite",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate copy/paste-ready fact posts."
    )

    parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        metavar="1-12",
        help="Month number to generate posts for. Defaults to today's month.",
    )

    parser.add_argument(
        "--day",
        type=int,
        choices=range(1, 32),
        metavar="1-31",
        help="Day number to generate posts for. Defaults to today's day.",
    )

    parser.add_argument(
        "--start-date",
        help="Start date for batch mode, formatted as YYYY-MM-DD.",
    )

    parser.add_argument(
        "--end-date",
        help="End date for batch mode, formatted as YYYY-MM-DD.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Number of facts to collect per category. Defaults to 3.",
    )

    parser.add_argument(
        "--max-posts",
        type=int,
        default=None,
        help=(
            "Maximum total number of posts to generate after collecting facts. "
            "Defaults to no total cap."
        ),
    )

    parser.add_argument(
        "--category",
        choices=VALID_CATEGORIES,
        action="append",
        help=(
            "Category to collect. Can be used more than once. "
            "Options: selected, events, births, deaths, holidays, all. "
            "Defaults to selected, events, and births."
        ),
    )

    parser.add_argument(
        "--tone",
        choices=VALID_TONES,
        default="witty",
        help=(
            "Tone for generated posts. Options: simple, witty, nostalgic, "
            "educational, engagement, snarky-lite. Defaults to witty."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Collect and display facts without generating AI posts or writing output.",
    )

    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomize collected facts before applying --max-posts.",
    )
    
    parser.add_argument(
        "--save-raw",
        action="store_true",
        help="Save selected raw facts to a text file before AI generation.",
    )
    
    return parser.parse_args()


def parse_iso_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as error:
        raise ValueError(f"Invalid date '{value}'. Use YYYY-MM-DD.") from error


def get_dates_to_process(args: argparse.Namespace) -> list[date]:
    today = datetime.now().date()

    if args.start_date or args.end_date:
        if not args.start_date or not args.end_date:
            raise ValueError("Both --start-date and --end-date are required for batch mode.")

        start = parse_iso_date(args.start_date)
        end = parse_iso_date(args.end_date)

        if end < start:
            raise ValueError("--end-date must be the same as or after --start-date.")

        dates = []
        current = start

        while current <= end:
            dates.append(current)
            current += timedelta(days=1)

        return dates

    month = args.month or today.month
    day = args.day or today.day

    return [date(today.year, month, day)]


def build_output_path(target_date: date, categories: list[str]) -> str:
    if len(categories) == 1:
        category_label = categories[0]
    else:
        category_label = "mixed"

    return f"output/{target_date.isoformat()}/{category_label}.txt"


# def apply_max_posts(facts: list, max_posts: int | None) -> list:
#     if max_posts is None:
#         return facts

#     if max_posts < 1:
#         raise ValueError("--max-posts must be 1 or higher.")

#     return facts[:max_posts]

def build_raw_output_path(target_date: date, categories: list[str]) -> str:
    if len(categories) == 1:
        category_label = categories[0]
    else:
        category_label = "mixed"

    return f"output/{target_date.isoformat()}/raw_{category_label}.txt"

def select_facts(
    facts: list,
    max_posts: int | None,
    randomize: bool,
) -> list:
    selected_facts = facts.copy()

    if randomize:
        random.shuffle(selected_facts)

    if max_posts is None:
        return selected_facts

    if max_posts < 1:
        raise ValueError("--max-posts must be 1 or higher.")

    return selected_facts[:max_posts]

def print_dry_run_facts(facts: list) -> None:
    print("")
    print("DRY RUN - no AI posts generated.")
    print("=" * 60)

    for index, fact in enumerate(facts, start=1):
        print("")
        print(f"{index}. {fact.title}")
        print(f"   Category: {fact.category}")
        print(f"   Date: {fact.date_label}")
        print(f"   Year: {fact.year}")
        print(f"   Fact: {fact.fact}")
        print(f"   Source: {fact.source_url}")

    print("")
    print("=" * 60)
    print(f"Dry run complete. Displayed {len(facts)} facts.")


def dedupe_facts(facts: list) -> list:
    seen = set()
    unique_facts = []

    for fact in facts:
        key = (
            fact.category,
            fact.title,
            fact.year,
            fact.source_url,
        )

        if key in seen:
            continue

        seen.add(key)
        unique_facts.append(fact)

    return unique_facts

def process_date(
    target_date: date,
    categories: list[str],
    limit: int,
    max_posts: int | None,
    tone: str,
    dry_run: bool,
    randomize: bool,
    save_raw: bool,
) -> None:
    output_path = build_output_path(target_date, categories)

    print("")
    print("=" * 60)
    print(f"Processing {target_date.isoformat()}")
    print(f"Categories: {', '.join(categories)}")
    print(f"Randomize facts: {randomize}")
    print(f"Tone: {tone}")
    print("=" * 60)

    facts = collect_default_facts(
        month=target_date.month,
        day=target_date.day,
        limit_per_category=limit,
        categories=categories,
    )

    if not facts:
        print("No facts found. Nothing to generate.")
        return

    collected_count = len(facts)
    
    
    facts = dedupe_facts(facts)
    deduped_count = len(facts)

    facts = select_facts(
        facts=facts,
        max_posts=max_posts,
        randomize=randomize,
    )

    print(f"Collected {collected_count} facts.")

    duplicates_removed = collected_count - deduped_count

    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate facts.")
        
    

    if randomize:
        print("Randomized collected facts before selection.")

    if max_posts is not None:
        print(f"Using {len(facts)} facts because --max-posts={max_posts}.")
    else:
        print(f"Using {len(facts)} facts.")

    if save_raw:
        raw_output_path = build_raw_output_path(target_date, categories)
        export_raw_facts(
            facts=facts,
            output_path=raw_output_path,
            target_date=target_date,
            categories=categories,
        )
        print(f"Raw facts written to: {raw_output_path}")
        
    if dry_run:
        print_dry_run_facts(facts)
        return

    print("Generating posts...")

    generated_posts = []

    for index, fact in enumerate(facts, start=1):
        print(f"[{index}/{len(facts)}] Generating: {fact.title}")

        try:
            post_text = generate_post(fact, tone=tone)

            if "Hashtags:" not in post_text or "#" not in post_text:
                print(f"Warning: generated post may be missing hashtags: {fact.title}")

            generated_posts.append((fact, post_text))

        except Exception as error:
            print(f"Failed to generate post for {fact.title}: {error}")

    if not generated_posts:
        print("No posts generated.")
        return

    export_posts(generated_posts, output_path)

    print(f"Done. Posts written to: {output_path}")


def main() -> None:
    args = parse_args()
    categories = args.category or DEFAULT_CATEGORIES

    try:
        dates_to_process = get_dates_to_process(args)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Dates to process: {len(dates_to_process)}")

    for target_date in dates_to_process:
        process_date(
            target_date=target_date,
            categories=categories,
            limit=args.limit,
            max_posts=args.max_posts,
            tone=args.tone,
            dry_run=args.dry_run,
            randomize=args.random,
            save_raw=args.save_raw,
        )

    print("")
    print("All done.")


if __name__ == "__main__":
    main()
    