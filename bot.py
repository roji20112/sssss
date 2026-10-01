import os
import pytesseract

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN غير موجود في GitHub Secrets")


# تحويل الأرقام
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

    # حذف fh_
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
        resize_keyboard=True,
        is_persistent=True
    )

    await update.message.reply_text(
        "مرحبا 👋\n\n"
        "اختار العملية:",
        reply_markup=markup
    )


# زر كتابة
async def writing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "text"

    await update.message.reply_text(
        "📝 ابعث النص الآن:"
    )


# زر صورة
async def image_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "image"

    await update.message.reply_text(
        "🖼️ ابعث الصورة الآن:"
    )


# استقبال النصوص
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    # الأزرار
    if text == "📝 كتابة":
        await writing(update, context)
        return

    if text == "🖼️ صورة":
        await image_mode(update, context)
        return

    # إذا كتب المستخدم نص عادي
    result = convert_text(text)

    await update.message.reply_text(
        f"✅ النتيجة:\n{result}"
    )


# استقبال الصور
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return

    await update.message.reply_text("🔎 جاري قراءة الصورة...")

    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        image_path = "image.jpg"
        await file.download_to_drive(image_path)

        # OCR
        text = pytesseract.image_to_string(
            image_path,
            config="--psm 6"
        ).strip()

        if not text:
            await update.message.reply_text(
                "❌ لم أجد كتابة واضحة في الصورة."
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

    # أمر /start
    app.add_handler(CommandHandler("start", start))

    # استقبال الصور
    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    # استقبال النصوص والأزرار
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