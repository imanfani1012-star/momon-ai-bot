import os
import logging
import time
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from groq import Groq

# ===== CONFIG =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")  # HuggingFace (buat gambar)

client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(level=logging.INFO)

# ===== MEMORY =====
user_memory = {}
chat_history = {}
user_mode = {}

# ===== VOICE FUNCTION =====
def text_to_speech(text):
    url = "https://api.streamelements.com/kappa/v2/speech"
    params = {
        "voice": "Brian",
        "text": text
    }
    response = requests.get(url, params=params)
    return response.content

# ===== IMAGE FUNCTION =====
def generate_image(prompt):
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt})
    return response.content

# ===== COMMANDS =====
def start(update, context):
    update.message.reply_text("🔥 MOMON.AI aktif bro!\nKetik aja 😎")

def help_command(update, context):
    update.message.reply_text(
        "📌 COMMAND:\n"
        "/start\n"
        "/reset\n"
        "/history\n"
        "/mode [santai/serius/toxic]\n"
        "/voice [text]\n"
        "/img [prompt]\n"
    )

def reset(update, context):
    uid = update.message.chat_id
    user_memory.pop(uid, None)
    chat_history.pop(uid, None)
    update.message.reply_text("♻️ Memory dihapus!")

def history(update, context):
    uid = update.message.chat_id
    hist = chat_history.get(uid, [])
    if not hist:
        update.message.reply_text("Belum ada history.")
        return
    text = "\n".join([f"{m['role']}: {m['content']}" for m in hist[-5:]])
    update.message.reply_text(text)

def set_mode(update, context):
    uid = update.message.chat_id
    try:
        mode = context.args[0]
        user_mode[uid] = mode
        update.message.reply_text(f"🎭 Mode: {mode}")
    except:
        update.message.reply_text("Contoh: /mode santai")

# ===== VOICE COMMAND =====
def voice(update, context):
    try:
        text = " ".join(context.args)
        audio = text_to_speech(text)
        update.message.reply_voice(audio)
    except:
        update.message.reply_text("Error voice bro")

# ===== IMAGE COMMAND =====
def img(update, context):
    try:
        prompt = " ".join(context.args)
        update.message.reply_text("🎨 Lagi gambar...")
        image = generate_image(prompt)
        update.message.reply_photo(photo=image)
    except:
        update.message.reply_text("Error generate gambar bro")

# ===== CHAT AI =====
def chat(update, context):
    uid = update.message.chat_id
    user_text = update.message.text

    try:
        context.bot.send_chat_action(chat_id=uid, action=ChatAction.TYPING)
        time.sleep(1)

        # SIMPAN NAMA
        if "nama aku" in user_text.lower():
            name = user_text.split("nama aku")[-1].strip()
            user_memory[uid] = name
            update.message.reply_text(f"Siap {name} 😎")
            return

        name = user_memory.get(uid, "bro")
        mode = user_mode.get(uid, "santai")

        if mode == "toxic":
            style = "Sarkas, nyolot tapi lucu."
        elif mode == "serius":
            style = "Serius dan jelas."
        else:
            style = "Santai dan gaul."

        if uid not in chat_history:
            chat_history[uid] = []

        chat_history[uid].append({"role": "user", "content": user_text})
        chat_history[uid] = chat_history[uid][-10:]

        messages = [{
            "role": "system",
            "content": f"MOMON.AI, panggil {name}. {style}"
        }] + chat_history[uid]

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile"
        )

        reply = response.choices[0].message.content
        chat_history[uid].append({"role": "assistant", "content": reply})

        update.message.reply_text(reply)

    except Exception as e:
        logging.error(e)
        update.message.reply_text("⚠️ Error bro")

# ===== MAIN =====
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(CommandHandler("mode", set_mode))
    dp.add_handler(CommandHandler("voice", voice))
    dp.add_handler(CommandHandler("img", img))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    print("🚀 BOT FULL FITUR NYALA")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
