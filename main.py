import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq

# ================== CONFIG ==================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ================== LOGGING ==================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================== COMMAND ==================
def start(update, context):
    update.message.reply_text("🔥 Halo bro gue MOMON.AI\nTanya apa aja santai 😎")

# ================== CHAT AI ==================
def chat(update, context):
    try:
        user_message = update.message.text
        print("USER:", user_message)

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Lo adalah MOMON.AI, bot gaul, santai, kadang lucu."},
                {"role": "user", "content": user_message}
            ],
            model="mixtral-8x7b-32768"
        )

        ai_reply = response.choices[0].message.content
        print("AI:", ai_reply)

        update.message.reply_text(ai_reply)

    except Exception as e:
        print("ERROR:", e)
        update.message.reply_text("⚠️ Waduh error bro, coba lagi nanti.")

# ================== MAIN ==================
def main():
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN belum di set")
        return

    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY belum di set")
        return

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
