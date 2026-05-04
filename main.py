import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

TELEGRAM_TOKEN = os.environ.get("8025930923:AAFtdj8UE8kHbF18_5DL7OQI4l0GMJDU0N0")
GROQ_KEY = os.environ.get("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")

client = Groq(api_key=GROQ_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo bro gue MOMON.AI 🔥 Udah online 24/7 di Railway')

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": update.message.text}]
    )
    await update.message.reply_text(response.choices[0].message.content)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
