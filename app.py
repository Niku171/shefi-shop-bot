import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Το bot δουλεύει 24/7 🚀")

application.add_handler(CommandHandler("start", start))

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    application.run_polling()
