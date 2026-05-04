import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq

# ===== CONFIG =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ===== START =====
def start(update, context):
    update.message.reply_text(
        "🔥 Halo bro gue MOMON.AI\n"
        "💬 Chat bebas\n"
        "🖼 Ketik: /gambar kucing lucu\n"
    )

# ===== CHAT AI =====
def chat(update, context):
    user_message = update.message.text
    print("USER:", user_message)

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Lu adalah MOMON.AI, bot santai, gaul Indonesia."},
                {"role": "user", "content": user_message}
            ],
            model="llama3-8b-8192"
        )

        ai_reply = response.choices[0].message.content
        print("BOT:", ai_reply)

        update.message.reply_text(ai_reply)

    except Exception as e:
        print("ERROR:", e)
        update.message.reply_text("⚠️ Waduh error bro, coba lagi nanti.")

# ===== GAMBAR GRATIS =====
def gambar(update, context):
    try:
        prompt = " ".join(context.args)

        if not prompt:
            update.message.reply_text("Contoh: /gambar kucing lucu")
            return

        # API GRATIS
        url = f"https://image.pollinations.ai/prompt/{prompt}"

        update.message.reply_text("🎨 Lagi bikin gambar...")

        update.message.reply_photo(url)

    except Exception as e:
        print("ERROR GAMBAR:", e)
        update.message.reply_text("❌ Gagal bikin gambar bro.")

# ===== MAIN =====
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gambar", gambar))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    print("✅ Bot nyala bro...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
