import os
import pytesseract

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN غير موجود في GitHub Secrets")


# التحويل
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


def convert_text(text):
    text = text.strip()

    # حذف fh_ من البداية
    if text.startswith("fh_"):
        text = text[3:]

    result = ""

    for char in text:
        result += convert.get(char, char)

    return f"wlan{result}"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📝 كتابة", "🖼️ صورة"]
    ]

    markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "مرحبا 👋\n"
        "اختار واش حاب تدير:",
        reply_markup=markup
    )


# زر الكتابة
async def writing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "text"

    await update.message.reply_text(
        "📝 ابعثلي النص الآن، ونحوّلهولك."
    )


# زر الصورة
async def image_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "image"

    await update.message.reply_text(
        "🖼️ ابعثلي الصورة الآن، وأنا نقرأ الكتابة اللي فيها ونحوّلها."
    )


# استقبال النص
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if text == "📝 كتابة":
        await writing(update, context)
        return

    if text == "🖼️ صورة":
        await image_mode(update, context)
        return

    result = convert_text(text)

    await update.message.reply_text(result)


# استقبال الصور
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return

    await update.message.reply_text("🔎 جاري قراءة الصورة...")

    try:
        # أخذ أعلى جودة للصورة
        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        image_path = "image.jpg"

        await file.download_to_drive(image_path)

        # قراءة النص من الصورة
        text = pytesseract.image_to_string(
            image_path,
            config="--psm 6"
        ).strip()

        if not text:
            await update.message.reply_text(
                "❌ ما قدرتش نلقى كتابة واضحة في الصورة."
            )
            return

        result = convert_text(text)

        await update.message.reply_text(
            f"📄 النص المقروء:\n{text}\n\n"
            f"✅ النتيجة:\n{result}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ حدث خطأ:\n{e}"
        )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # /start
    app.add_handler(
        MessageHandler(
            filters.COMMAND & filters.Regex(r"^/start$"),
            start
        )
    )

    # الصور
    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    # النصوص والأزرار
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()