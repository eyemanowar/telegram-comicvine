# Telegram ComicVine Bot

A Telegram bot that fetches and formats weekly comic book releases from ComicVine API, helping comic book enthusiasts track new issues and series.

## Features

- **Automated Release Tracking**: Fetches weekly comic releases from ComicVine API based on store dates
- **Smart Filtering**: Distinguishes between new series debuts (issue #1) and ongoing series
- **Reading List Integration**: Cross-references releases with your personal comic database from ComicsHelper
- **Telegraph Publishing**: Formats and publishes releases to Telegraph for easy reading
- **API Integration**: Backend deployed on PythonAnywhere for reliable access

## Tech Stack

- **Python 3.x**
- **python-telegram-bot**: Telegram Bot API wrapper
- **requests**: HTTP library for API calls
- **Flask**: Backend API framework
- **Telegraph API**: Content publishing

## Project Structure

```
telegram-comicvine/
├── bot.py              # Telegram bot entry point
├── comic_vine.py       # ComicVine API integration & data processing
├── api_handler.py      # Generic API request handler
├── telegraph.py        # Telegraph API integration
├── flask_app.py        # Backend API endpoint
├── time_helper.py      # Date/time utilities
└── content.json        # Cached comic data
```

## Key Components

### ComicVine Integration (`comic_vine.py`)
- Fetches issues by store date using ComicVine API
- Parses and cleans HTML descriptions
- Categorizes comics into:
  - **New Series**: First issues (#1) 
  - **Continuous Series**: Ongoing series from your reading list

### Bot Functionality (`bot.py`)
- Telegram bot interface for user commands
- Backend API: `https://eyemanowar.pythonanywhere.com/api/latest-releases`

## Setup

1. Install dependencies:
```bash
pip install python-telegram-bot requests python-dotenv Flask
```

2. Set environment variables:
```bash
export COMICVINE_API_KEY='your_comicvine_api_key'
```

3. Configure bot token in `bot.py` (use environment variable in production)

4. Run the bot:
```bash
python bot.py
```

## Usage

The bot cross-references ComicVine releases with your personal reading list from ComicsHelper, automatically highlighting:
- New series starting this week
- Issues from series you're following
- Cover images and descriptions

## API Response Format

Telegraph-formatted JSON with structured content:
```json
[
  {"tag": "b", "children": ["Series Name #1"]},
  {"tag": "img", "attrs": {"src": "cover_url"}},
  {"tag": "p", "children": ["Description text"]}
]
```

## Integration with ComicsHelper

References the comic database at:
```
/Users/{user_name}/{path to ComicsHelper/database}/database.json
```

Only highlights issues from series in your reading list.

## Future Enhancements

- [ ] User authentication and personalized reading lists
- [ ] Push notifications for followed series
- [ ] Search functionality for specific comics
- [ ] Weekly digest summaries

## License

Personal project - educational purposes

## Author

Oleksii Kolumbet
