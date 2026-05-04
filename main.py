import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo bro gue MOMON.AI 🔥 Ada yang bisa gue bantu?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Lo adalah MOMON.AI, bot gaul yang to the point dan suka pake 'bro'."},
            {"role": "user", "content": user_message}
        ],
        model="llama3-8b-8192",
    )
    ai_reply = response.choices[0].message.content
    await update.message.reply_text(ai_reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot nyala bro...")
    app.run_polling()
