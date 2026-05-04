import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq

# ================== CONFIG ==================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ================== LOGGING ==================
logging.basicConfig(level=logging.INFO)

# ================== COMMAND ==================
def start(update, context):
    update.message.reply_text("Halo bro gue MOMON.AI 🔥 Ada yang bisa gue bantu?")

# ================== CHAT AI ==================
def chat(update, context):
    try:
        user_message = update.message.text
        print("USER:", user_message)

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Lu adalah MOMON.AI, bot santai, gaul, dan suka bantu orang."},
                {"role": "user", "content": user_message}
            ]
        )

        print("RAW:", response)

        ai_reply = response.choices[0].message.content

        if not ai_reply:
            ai_reply = "Gue bingung jawabnya bro 😅"

        update.message.reply_text(ai_reply)

    except Exception as e:
        print("ERROR:", e)
        update.message.reply_text(f"ERROR: {e}")

# ================== MAIN ==================
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    print("✅ Bot nyala bro...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
