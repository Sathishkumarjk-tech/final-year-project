from telegram.ext import Updater, MessageHandler, Filters
from config import TELEGRAM_BOT_TOKEN
from utils import internet_available

def handle(update, context):
    text = update.message.text
    print(f"[Telegram] {text}")

def run_bot():
    if not internet_available():
        print("📴 Telegram disabled (no internet)")
        return

    try:
        updater = Updater(
            token=8529956626:AAHsYh40oWK7UYNbtFY25e5FrrOcCPWqCV0,
            use_context=True)
        

        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))

        print("📱 Telegram bot started")
        updater.start_polling()

        # ❌ DO NOT CALL updater.idle()
        # This avoids signal() crash in thread

    except Exception as e:
        print(f"⚠ Telegram stopped: {e}")
