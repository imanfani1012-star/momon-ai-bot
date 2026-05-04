import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq

# ================== LOGGING ==================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

print("STARTING BOT...")

# ================== ENV ==================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN belum diset!")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY belum diset!")

# ================== GROQ ==================
client = Groq(api_key=GROQ_API_KEY)

# ================== COMMAND ==================
def start(update, context):
    update.message.reply_text("Halo bro gue MOMON.AI 🔥 Ada yang bisa gue bantu?")

# ================== CHAT ==================
def chat(update, context):
    try:
        user_message = update.message.text

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Lo adalah MOMON.AI, bot santai, gaul, jawab singkat tapi jelas."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama3-70b-8192",
        )

        ai_reply = response.choices[0].message.content
        update.message.reply_text(ai_reply)

    except Exception as e:
        logging.error(f"ERROR: {e}")
        update.message.reply_text("⚠️ Error bro, coba lagi nanti.")

# ================== MAIN ==================
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    print("✅ Bot nyala bro...")
    updater.start_polling()
    updater.idle()

# ================== RUN ==================
if __name__ == "__main__":
    main()
