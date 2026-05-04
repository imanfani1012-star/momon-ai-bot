from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from groq import Groq
import os

# ambil env
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# client groq
client = Groq(api_key=GROQ_API_KEY)

# start command
def start(update, context):
    update.message.reply_text("🔥 Halo bro gue MOMON.AI\nTanya apa aja santai 😎")

# handle chat
def handle(update, context):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Lu adalah AI santai, jawab kayak anak nongkrong."},
                {"role": "user", "content": user_text}
            ],
            model="mixtral-8x7b-32768"  # model aman (TIDAK ERROR)
        )

        reply = response.choices[0].message.content
        update.message.reply_text(reply)

    except Exception as e:
        print("ERROR:", e)
        update.message.reply_text("⚠️ Waduh error bro, coba lagi nanti")

# main bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))

    print("✅ Bot nyala bro...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
