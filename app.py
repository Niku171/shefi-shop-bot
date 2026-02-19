import os
import sqlite3
import stripe
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =====================
# ENV VARIABLES
# =====================

TOKEN = os.environ.get("BOT_TOKEN")
STRIPE_SECRET = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

stripe.api_key = STRIPE_SECRET

bot = Bot(token=TOKEN)
app = Flask(__name__)

# =====================
# DATABASE
# =====================

def init_db():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    product TEXT,
                    duration TEXT,
                    payment_id TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

# =====================
# TELEGRAM START
# =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
              (user.id, user.username))
    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"👋 Hi {user.first_name}\n\nWelcome to SHEFI SHOP 🚀"
    )

# =====================
# STRIPE WEBHOOK
# =====================

@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return str(e), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = int(session["metadata"]["user_id"])
        product = session["metadata"]["product"]
        duration = session["metadata"]["duration"]

        conn = sqlite3.connect("shop.db")
        c = conn.cursor()
        c.execute("INSERT INTO orders (user_id, product, duration, payment_id) VALUES (?, ?, ?, ?)",
                  (user_id, product, duration, session["id"]))
        conn.commit()
        conn.close()

        bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment Received!\n\nProduct: {product}\nDuration: {duration}"
        )

        bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💰 New Order\nUser: {user_id}\nProduct: {product}\nDuration: {duration}"
        )

    return "OK", 200

# =====================
# WEBHOOK ROUTE
# =====================

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.process_update(update)
    return "ok"

# =====================
# MAIN
# =====================

if __name__ == "__main__":
    app.run()
