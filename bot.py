from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8796899863:AAHbd1Jaz6g1UDQSsublG9ctgBHYAUd-v5M"

convert = {
    "1": "e",
    "0": "f",
    "2": "d",
    "3": "c",
    "4": "b",
    "5": "a",
    "6": "9",
    "7": "8",
    "8": "7",
    "9": "6"
}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # حذف fh_
    if text.startswith("fh_"):
        text = text[3:]

    result = ""

    for char in text:
        result += convert.get(char, char)

    final_text = f"wlan{result}"

    await update.message.reply_text(final_text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot Started...")
app.run_polling()