import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def start(update, context):
    update.message.reply_text("Halo bro gue MOMON.AI 🔥 Ada yang bisa gue bantu?")

def chat(update, context):
    user_message = update.message.text
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Lo adalah MOMON.AI, bot gaul yang to the point dan suka pake 'bro'."},
            {"role": "user", "content": user_message}
        ],
        model="llama3-8b-8192",
    )
    ai_reply = response.choices[0].message.content
    update.message.reply_text(ai_reply)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))
    print("Bot nyala bro...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
