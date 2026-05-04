import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq

# ====== CONFIG ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ====== COMMAND ======
def start(update, context):
    update.message.reply_text("🔥 Halo bro gue MOMON.AI\nTanya apa aja santai 😎")

# ====== CHAT ======
def chat(update, context):
    try:
        user_message = update.message.text

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Lu adalah MOMON.AI, bot santai, gaul, bahasa Indonesia."},
                {"role": "user", "content": user_message}
            ],
            model="llama3-8b-8192"  # ✅ GANTI KE INI (AMAN)
        )

        ai_reply = response.choices[0].message.content
        update.message.reply_text(ai_reply)

    except Exception as e:
        print("ERROR:", e)
        update.message.reply_text("⚠️ Waduh error bro, coba lagi nanti.")

# ====== MAIN ======
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
