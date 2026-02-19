import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Παίρνουμε το token από τα Environment Variables του Render
TOKEN = os.environ.get("BOT_TOKEN")

# STRIPE LINKS
S1 = "https://buy.stripe.com/eVq5kD0Pz5b1e6FduJ2Nq00"
S7 = "https://buy.stripe.com/6oUdR9gOx46X4w5eyN2Nq02"
S15 = "https://buy.stripe.com/6oU14n2XH1YPe6F4Yd2Nq03"
S31 = "https://buy.stripe.com/6oU14n2XH1YPe6F4Yd2Nq03"

I1 = "https://buy.stripe.com/dRm4gz41LdHx7IhcqF2Nq06"
I7 = "https://buy.stripe.com/5kQ9ATdCl6f52nX62h2Nq05"
I31 = "https://buy.stripe.com/cNiaEXgOx9rh0fP3U92Nq01"

# START MESSAGE
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name

    keyboard = [
        [InlineKeyboardButton("🛍 Shop Now", callback_data="shop")]
    ]

    text = f"""
🔥 *Welcome to SHEFI SHOP*

Hi {user_name} 👋

✨ Instant Delivery 24/7  
🔒 100% Secure Payment  
💎 Best Prices Guaranteed  

📱 Android & iOS
"""

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# BUTTON HANDLER
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "shop":
        keyboard = [
            [InlineKeyboardButton("📱 Samsung", callback_data="samsung")],
            [InlineKeyboardButton("🍏 iOS", callback_data="ios")],
            [InlineKeyboardButton("🔙 Back", callback_data="home")]
        ]

        await query.edit_message_text(
            "🛍 *Select Your Platform:*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "samsung":
        keyboard = [
            [InlineKeyboardButton("1 Day - 2€", url=S1)],
            [InlineKeyboardButton("7 Days - 7€", url=S7)],
            [InlineKeyboardButton("15 Days - 12€", url=S15)],
            [InlineKeyboardButton("31 Days - 17€", url=S31)],
            [InlineKeyboardButton("🔙 Back", callback_data="shop")]
        ]

        await query.edit_message_text(
            "📱 *Samsung – Drip Client*\n\nSelect Duration:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "ios":
        keyboard = [
            [InlineKeyboardButton("1 Day - 7€", url=I1)],
            [InlineKeyboardButton("7 Days - 17€", url=I7)],
            [InlineKeyboardButton("31 Days - 27€", url=I31)],
            [InlineKeyboardButton("🔙 Back", callback_data="shop")]
        ]

        await query.edit_message_text(
            "🍏 *iOS – Fluorite*\n\nSelect Duration:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "home":
        await start(update, context)

# MAIN
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running 24/7...")
    app.run_polling()
