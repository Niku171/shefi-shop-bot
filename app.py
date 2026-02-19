import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")

# Flask server (για Render)
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Telegram command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Το bot λειτουργεί 24/7 🚀")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    Thread(target=run_web).start()
    run_bot()
