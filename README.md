# Social Media Fact Post Creator

A small Python tool that collects factual "On This Day" style data, sends it to OpenAI, and writes copy/paste-ready social posts to plain text files.

No social media posting.
No scheduling.
No Facebook integration.
No platform automation.

Just:

```text
facts in → AI-written posts out → copy/paste manually
```

## What It Does

The app currently uses Wikimedia/Wikipedia's On This Day feed to collect factual data, then asks OpenAI to turn that data into short Facebook-style posts.

Generated posts include:

- a short written post
- hashtags
- a source link
- dated output folders
- category-specific output files

## Current Features

- Generate posts for today's date by default
- Generate posts for a specific month and day
- Generate posts across a date range
- Select one or more fact categories
- Select post tone
- Limit total number of generated posts
- Randomize selected facts before generation
- Dry-run mode to preview facts without using OpenAI
- Plain `.txt` output for easy copy/paste
- Strict output format requiring hashtags and source links

## Current Data Source

The current version uses Wikimedia/Wikipedia On This Day data.

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

## Project Structure

```text
sm-post-creator/
│
├── output/
│   └── YYYY-MM-DD/
│       ├── mixed.txt
│       ├── births.txt
│       └── events.txt
│
├── src/
│   ├── ai_writer.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── post_exporter.py
│   └── wikimedia_collector.py
│
├── .env
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

On Windows PowerShell, use:

```bash
copy .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
APP_USER_AGENT=FactPostGenerator/0.1 (your-email@example.com)
```

## Run the App

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

Preview facts without calling OpenAI or writing output:

```bash
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --dry-run
```

Dry-run mode is useful before batch generation so you can inspect source facts before spending API calls.

## Randomize Facts

Randomize collected facts before applying `--max-posts`:

```bash
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --random
```

Useful when the same top results keep appearing.

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

Each post includes:

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
python3 src/main.py --category births --month 5 --day 18 --limit 10 --max-posts 3 --random
```

Batch a few days:

```bash
python3 src/main.py --start-date 2026-05-18 --end-date 2026-05-20 --category births --limit 10 --max-posts 3 --random
```

## Important Notes

The AI writer is instructed to use only the factual data provided by the collector.

Still, always review generated posts before publishing.

This tool creates drafts, not final truth. Source links are included so posts can be checked quickly.

## Suggested Next Improvements

Possible future upgrades:

- save raw collected facts to text files
- add MusicBrainz collector for music-specific facts
- add movie data collector
- add duplicate detection
- add per-category tone defaults
- add output summaries
- add tests for collector/exporter behavior

## Current Status

Working MVP.

The current version is useful for generating copy/paste social posts from sourced historical and birthday data.
