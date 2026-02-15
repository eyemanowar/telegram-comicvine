import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv('BOT_KEY')
BACKEND_API_URL = "https://eyemanowar.pythonanywhere.com/api/latest-releases"

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # application.add_handler(CommandHandler("latest", latest_releases))

    application.run_polling()

main()