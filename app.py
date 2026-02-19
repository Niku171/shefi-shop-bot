import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

app = Flask(__name__)

application = ApplicationBuilder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Το bot δουλεύει 24/7 🚀")

application.add_handler(CommandHandler("start", start))

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

if __name__ == "__main__":
    import asyncio

    async def main():
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(f"{RENDER_EXTERNAL_URL}/{TOKEN}")

    asyncio.run(main())
    app.run(host="0.0.0.0", port=10000)
