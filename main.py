import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq

# ================== LOGGING ==================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

print("🚀 STARTING MOMON.AI BOT...")

# ================== ENV ==================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN belum diset!")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY belum diset!")

client = Groq(api_key=GROQ_API_KEY)

# ================== COMMAND ==================
def start(update, context):
    update.message.reply_text("Halo bro gue MOMON.AI 🔥 Ada yang bisa gue bantu?")

# ================== CHAT ==================
def chat(update, context):
    try:
        user_message = update.message.text

        response
