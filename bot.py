
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, CallbackQueryHandler, filters
from database_helper import DbHandler
from telegraph import Telegraph
from comic_vine import ComicVine
from time_helper import Date
from dotenv import load_dotenv
import json, csv, io, os, logging, asyncio

load_dotenv('keys.env')
BOT_TOKEN = os.getenv('BOT_KEY')
# BACKEND_API_URL = "https://eyemanowar.pythonanywhere.com/api/latest-releases"

ASK_SERIES, ASK_MORE = range(2)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Bot:

    def __init__(self):
        self.db = DbHandler()
        self.db.init_db()
        self.comicvine = ComicVine()
        self.tg = Telegraph()
        self.date = Date()
        self.main_menu = ReplyKeyboardMarkup(
            [["📅 Releases", "📋 List", "➕ Add", "➖ Remove"]],
            resize_keyboard=True,
            # one_time_keyboard=True,
            input_field_placeholder="Choose an action"
        )
        self.yes_no = ReplyKeyboardMarkup(
            [["Yes", "No"]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.db.add_user(user.id, user.username)
        await update.message.reply_text(f"Hi {user.username}!")
        await update.message.reply_text("""
        📚 Managing your reading list

➕ ADD SERIES
Tap "➕ Add", then either:
• Type series names — one per line
• Or upload a file (.json or .csv)

➖ REMOVE SERIES
Tap "➖ Remove", then type or upload the series to remove (same formats).

📄 FILE FORMATS
• .json — an object where each series name is a key:
     {"batman": {}, "spider-man": {}}
• .csv — one series per row, in the first column
  (a header row like "title" is skipped):
     batman
     spider-man

✍️ TIPS
• Capitalization doesn't matter — names are stored in lowercase.
• Typing several? Put each on its own line — not commas
  (some titles contain commas).
• After each add/remove, tap "Yes" to continue or "No" to finish.
""")
        await update.message.reply_text("Choose an option:", reply_markup=self.main_menu)

    async def list_series(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        reading_list = self.db.get_reading_list(user.id)
        if not reading_list:
            await update.message.reply_text(f"List is empty. Add series", reply_markup=self.main_menu)
        else:
            series = "\n".join(f"• {x}".title() for x in reading_list)
            await update.message.reply_text(f'Your list is:\n{series}', reply_markup=self.main_menu)

    async def start_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['mode'] = 'add'
        await update.message.reply_text("Type a series:")
        return ASK_SERIES

    async def start_remove(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['mode'] = 'remove'
        await update.message.reply_text("Type a series to remove:")
        return ASK_SERIES

    async def handling_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        doc = update.message.document
        file = await context.bot.get_file(doc.file_id)  # fetch file handle from Telegram
        content = await file.download_as_bytearray()
        text = content.decode('utf-8')
        name = (doc.file_name or "")
        if name.endswith(".json"):
            try:
                data = json.loads(text)
                series = data.keys()
            except json.JSONDecodeError:
                await update.message.reply_text(f"Uploaded file is not valid JSON")
                return ASK_SERIES
        elif name.endswith(".csv"):
            comics = csv.reader(io.StringIO(text))
            series = []
            for comic in comics:
                if not comic:
                    continue
                if comic[0] in ('title', 'Title', 'Series', 'series', 'Ongoing', 'ongoing'):
                    continue
                series.append(comic[0])
        else:
            await update.message.reply_text("Please send a .json or .csv file")
            return ASK_SERIES
        if context.user_data['mode'] == 'add':
            processed_comics = self.db.add_many(user.id, series)
            await update.message.reply_text(f"{processed_comics} was/were processed.\nAdd more series?", reply_markup=self.yes_no)
            return ASK_MORE
        else:
            processed_comics = self.db.remove_many(user.id, series)
            await update.message.reply_text(f"{processed_comics} was/were processed.\nRemove more series?", reply_markup=self.yes_no)
            return ASK_MORE

    async def handling_series(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        series = update.message.text.lower()
        if context.user_data['mode'] == 'add':
            processed_comics = self.db.add_many(user.id, series)
            await update.message.reply_text(f"{processed_comics} was/were processed.\nAdd more series?", reply_markup=self.yes_no)
            return ASK_MORE
        else:
            processed_comics = self.db.remove_many(user.id, series)
            await update.message.reply_text(f"{processed_comics} was/were processed.\nRemove more series?", reply_markup=self.yes_no)
            return ASK_MORE

    async def handling_more(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "Yes":
            if context.user_data['mode'] == 'add':
                await update.message.reply_text("Upload a JSON file or type a series to add:")
                return ASK_SERIES
            else:
                await update.message.reply_text("Type a series to remove:")
                return ASK_SERIES
        else:
            await update.message.reply_text("Done!", reply_markup=self.main_menu)
            return ConversationHandler.END

    async def cancel(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Cancelled.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    async def get_new_releases(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        week = self.date.get_the_current_week()
        await update.message.reply_text("Getting new releases...")
        content = await asyncio.to_thread(self.comicvine.get_new_issues, week, user.id)
        result = await asyncio.to_thread(self.tg.make_post, content)
        if not result:
            await update.message.reply_text("No releases were found")
        else:
            await update.message.reply_text(f"Here's your pull list for this week:\n{result['result']['url']}")
        return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    bot = Bot()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", bot.start))

    application.add_handler(MessageHandler(filters.Text(["📅 Releases"]), bot.get_new_releases))

    application.add_handler(MessageHandler(filters.Text(["📋 List"]), bot.list_series))

    handling_series = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text(["➕ Add"]), bot.start_add),
            MessageHandler(filters.Text(["➖ Remove"]), bot.start_remove),
        ],
        states={
            ASK_SERIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handling_series),
                         MessageHandler(filters.Document.FileExtension("json"), bot.handling_document),],
            ASK_MORE: [MessageHandler(filters.Text(["Yes", "No"]), bot.handling_more)]
        },
        fallbacks=[CommandHandler("cancel", bot.cancel)],
    )

    application.add_handler(handling_series)

    # application.add_handler(MessageHandler(filters.Text(["➖ Remove"]), bot.remove_flow))

    # application.add_handler(CommandHandler("latest", latest_releases))

    application.run_polling()

main()