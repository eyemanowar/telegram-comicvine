import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_KEY')
BACKEND_API_URL = "https://eyemanowar.pythonanywhere.com/api/latest-releases"


logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Click Me", callback_data="btn_clicked")],
        [InlineKeyboardButton("Option A", callback_data="a"),
         InlineKeyboardButton("Option B", callback_data="b")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # removes the "loading" state on button

    if query.data == "btn_clicked":
        await query.edit_message_text("You clicked the main button!")
    elif query.data == "a":
        await query.edit_message_text("You picked Option A")
    elif query.data == "b":
        await query.edit_message_text("You picked Option B")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # application.add_handler(CommandHandler("latest", latest_releases))

    application.run_polling()

print(repr(BOT_TOKEN))
# main()