# Social Media Fact Post Creator

A Python tool that collects sourced factual data and turns it into copy/paste-ready social media posts.

No auto-posting.
No scheduling.
No Facebook API.
No platform integrations.

Just:

```text
collect facts → generate posts → save .txt files → copy/paste manually
```

## Current Status

Working MVP.

The current version collects "On This Day" style data from Wikimedia/Wikipedia, sends selected facts to OpenAI, and writes social-ready posts to plain text files.

The generated posts include:

- short post text
- hashtags
- source links
- dated output folders
- optional raw fact files for auditing

## Why This Exists

The goal is to quickly create reviewable social media post drafts based on sourced facts.

This is useful for:

- music trivia pages
- movie trivia pages
- history posts
- famous birthday posts
- "On This Day" style content
- general Facebook/social media engagement posts

The tool does not publish anything. You stay in control and review before posting.

## Features

- Generate posts for today's date by default
- Generate posts for a specific month/day
- Generate posts across a date range
- Select one or more categories
- Select a writing tone
- Limit total generated posts
- Randomize selected facts
- Preview facts with dry-run mode
- Save raw selected facts
- Save posts as plain `.txt`
- Include source links
- Enforce hashtag output
- Keep generated output out of Git

## Current Data Source

This version uses Wikimedia/Wikipedia's On This Day feed.

Supported categories:

```text
selected
events
births
deaths
holidays
all
```

Default categories:

```text
selected
events
births
```

## Requirements

- Python 3.10+
- OpenAI API key
- Internet connection

## Project Structure

```text
sm-post-creator/
│
├── output/
│   └── YYYY-MM-DD/
│       ├── mixed.txt
│       ├── births.txt
│       ├── events.txt
│       └── raw_births.txt
│
├── src/
│   ├── ai_writer.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── post_exporter.py
│   └── wikimedia_collector.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```bash
copy .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
APP_USER_AGENT=FactPostGenerator/0.1 (your-email@example.com)
```

### About `APP_USER_AGENT`

`APP_USER_AGENT` identifies your script when it requests Wikimedia data.

It is not a secret key.

Example:

```env
APP_USER_AGENT=FactPostGenerator/0.1 (your-email@example.com)
```

## Basic Usage

Generate posts for today's date using the default categories:

```bash
python3 src/main.py
```

Generate birthday posts for a specific date:

```bash
python3 src/main.py --month 5 --day 18 --category births
```

Generate event posts for a specific date:

```bash
python3 src/main.py --month 5 --day 18 --category events
```

Generate multiple selected categories:

```bash
python3 src/main.py --month 5 --day 18 --category births --category events
```

## Batch Date Range

Generate posts for several dates:

```bash
python3 src/main.py --start-date 2026-05-18 --end-date 2026-05-24 --category births --limit 10 --max-posts 3
```

This creates one dated output folder per day:

```text
output/2026-05-18/births.txt
output/2026-05-19/births.txt
output/2026-05-20/births.txt
```

## Dry Run

Preview selected facts without calling OpenAI or writing generated post output:

```bash
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --dry-run
```

Dry-run mode is useful before batch generation so you can inspect facts before spending API calls.

## Randomize Facts

Randomize collected facts before applying `--max-posts`:

```bash
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --random
```

Useful when the same top results keep appearing.

## Save Raw Facts

Save selected raw facts before AI generation:

```bash
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --random --save-raw
```

Example output:

```text
output/2026-05-18/raw_births.txt
output/2026-05-18/births.txt
```

Raw fact files are useful for auditing generated posts later.

## Tone Options

Available tones:

```text
simple
witty
nostalgic
educational
engagement
snarky-lite
```

Example:

```bash
python3 src/main.py --category events --month 5 --day 18 --tone nostalgic
```

## Limit Output

`--limit` controls how many facts are collected per category.

```bash
python3 src/main.py --category births --limit 10
```

`--max-posts` controls how many total posts are generated after collection.

```bash
python3 src/main.py --category births --category events --limit 10 --max-posts 5
```

That command may collect up to 20 facts, but only generate 5 posts.

## Output

Generated posts are written to:

```text
output/YYYY-MM-DD/category.txt
```

Examples:

```text
output/2026-05-17/mixed.txt
output/2026-05-18/births.txt
output/2026-05-18/events.txt
```

Each generated post includes:

```text
POST #
CATEGORY
TITLE
DATE
YEAR
SOURCE

Post:
...

Hashtags:
...

Source:
...
```

## Recommended Quick Checks

Dry-run a small batch:

```bash
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --random --dry-run
```

Generate a small real batch:

```bash
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --random --save-raw
```

Batch a few days:

```bash
python3 src/main.py --start-date 2026-05-18 --end-date 2026-05-20 --category births --limit 10 --max-posts 3 --random --save-raw
```

## Git Ignore Notes

Generated output should not be committed.

Recommended `.gitignore` section:

```gitignore
# Generated output
output/
!output/.gitkeep
```

## Important Notes

The AI writer is instructed to use only the factual data provided by the collector.

Still, always review generated posts before publishing.

This tool creates drafts, not final truth. Source links are included so posts can be checked quickly.

## Roadmap

Possible future improvements:

- MusicBrainz collector for music-specific posts
- movie data collector
- duplicate history across previous runs
- per-category tone defaults
- output summaries
- tests for collector/exporter behavior
- optional markdown export
- optional CSV export

## Support

If this saved you some time and you feel like tossing a coffee my way, it is always appreciated:

[Buy me a coffee via PayPal](https://paypal.me/edwynsaunders1)


## License
MIT

