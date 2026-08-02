# Telegram ComicVine Bot

A multi-user Telegram bot that fetches weekly comic book releases from the ComicVine API, filters them against each user's personal reading list, and publishes a formatted digest to Telegraph.

## Features

- **Multi-user**: each Telegram user has their own reading list, stored in SQLite
- **Reading list management**: add, list, and remove series via an interactive reply keyboard
- **Bulk import**: upload your library as free text (one per line), a `.json` file, or a `.csv` file
- **Weekly releases**: `/releases` runs the pipeline for the user's list and returns a Telegraph link
- **Smart filtering**: distinguishes new series debuts (issue #1) from ongoing series you follow
- **Telegraph publishing**: formats releases (cover images, cleaned descriptions) into a Telegraph article

## Tech Stack

- **Python 3.12**
- **python-telegram-bot** — Telegram Bot API wrapper (async)
- **requests** — HTTP calls to ComicVine and Telegraph
- **SQLite** (`sqlite3`, stdlib) — per-user reading lists
- **python-dotenv** — configuration/secrets loading
- **Flask** — optional backend API (not required to run the bot)
- **pytest** — test suite

## Project Structure

```
telegram-comicvine/
├── bot.py              # Telegram bot — handlers, menus, entry point
├── comic_vine.py       # ComicVine API integration & release filtering
├── api_handler.py      # Generic HTTP request handler
├── telegraph.py        # Telegraph publishing
├── database_helper.py  # SQLite schema + reading-list data access
├── time_helper.py      # Week date-range helpers
├── main.py             # Standalone pipeline runner (non-bot)
├── flask_app.py        # Optional Flask API
├── conftest.py         # pytest path setup
└── tests/              # unit tests (time_helper, comic_vine, api_handler, database_helper)
```

## Data Model (SQLite)

- `users` — one row per Telegram user (`id` = chat_id, `username`, `created_at`)
- `reading_list` — one row per (user, series); `UNIQUE(user_id, series_name)`, foreign key to `users`

Series names are stored lowercase for case-insensitive matching against ComicVine.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `keys.env` file (copy the template and fill in your values):
```bash
cp keys.env.example keys.env
```
Required variables:
```
BOT_KEY=            # Telegram bot token from @BotFather
COMICVINE_API_KEY=  # https://comicvine.gamespot.com/api/
TELEGRAPH_API_KEY=  # https://api.telegra.ph/createAccount
SQLITE_PATH=        # e.g. comics.db
```

3. Run the bot:
```bash
python bot.py
```

The SQLite tables are created automatically on first run.

## Bot Usage

- `/start` — register and show the menu
- **📋 List** — show your reading list
- **➕ Add** — type series (one per line) or upload a `.json` / `.csv` file
- **➖ Remove** — type or upload series to remove
- **📅 Releases** — fetch this week's releases for your list and get a Telegraph link

### Upload formats

- **JSON** — an object whose keys are series names: `{"batman": {}, "spider-man": {}}`
- **CSV** — one series per row in the first column (a `title` header row is skipped)
- **Text** — one series name per line

## Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Telegraph Content Format

Releases are serialized as Telegraph node JSON:
```json
[
  {"tag": "b", "children": ["Series Name #1"]},
  {"tag": "figure", "children": [
    {"tag": "img", "attrs": {"src": "cover_url"}},
    {"tag": "figcaption", "children": ["Series Name"]}
  ]},
  {"tag": "p", "children": ["Description text"]}
]
```

## Roadmap

- [x] Per-user reading lists (SQLite)
- [x] Bulk import (text / JSON / CSV)
- [x] On-demand weekly releases
- [ ] Recurring weekly digest (scheduled notifications)
- [ ] Filter modes (reading list / all / first issues / list + first)
- [ ] Settings menu
- [ ] Deployment (PythonAnywhere scheduled task, CI)

## License

Personal project — educational purposes

## Author

Oleksii Kolumbet
