import requests
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("7576261047:AAHXxkGR_GlRsGnWQMXhjeUrdPF3uRV_eMs")
SMM_API_KEY = os.getenv("599982cdb61350f8191cb798b1e9e304")
SMM_API_URL = os.getenv("https://smmapi.net/api/v2")

MARKUP = float(os.getenv("MARKUP", 2))


def calculate_price(price):
    return round(float(price) * MARKUP, 3)


def get_services():
    data = {
        "key": SMM_API_KEY,
        "action": "services"
    }

    response = requests.post(SMM_API_URL, data=data)
    return response.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    services = get_services()

    keyboard = []

    for service in services[:10]:

        original_price = float(service["rate"])
        display_price = calculate_price(original_price)

        keyboard.append([
            InlineKeyboardButton(
                f'{service["name"]} - {display_price}$',
                callback_data=str(service["service"])
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "8729",
        reply_markup=reply_markup
    )


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    service_id = query.data

    data = {
        "key": SMM_API_KEY,
        "action": "add",
        "service": service_id,
        "link": "https://example.com",
        "quantity": 100
    }

    response = requests.post(SMM_API_URL, data=data)

    await query.edit_message_text("تم ارسال الطلب بنجاح ✅")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(order))

app.run_polling()
