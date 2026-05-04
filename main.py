import os
import logging
import time
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from groq import Groq

# ===== CONFIG =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(level=logging.INFO)

# ===== DATABASE FILE =====
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

db = load_data()

# ===== MEMORY CHAT =====
chat_history = {}
user_mode = {}

# ===== GET USER =====
def get_user(uid):
    uid = str(uid)
    if uid not in db:
        db[uid] = {
            "limit": 10,
            "referrals": 0,
            "referred_by": None,
            "name": "bro"
        }
    return db[uid]

# ===== COMMANDS =====
def start(update, context):
    uid = str(update.message.chat_id)
    user = get_user(uid)

    # REFERRAL SYSTEM
    if context.args:
        ref_id = context.args[0]

        if ref_id != uid and user["referred_by"] is None:
            user["referred_by"] = ref_id

            ref_user = get_user(ref_id)
            ref_user["referrals"] += 1
            ref_user["limit"] += 5

            context.bot.send_message(
                chat_id=int(ref_id),
                text="🎉 Referral masuk! +5 limit 😎"
            )

            save_data(db)

    bot_username = context.bot.username
    ref_link = f"https://t.me/{bot_username}?start={uid}"

    update.message.reply_text(
        f"🔥 MOMON.AI aktif bro!\n\n"
        f"Limit: {user['limit']}\n"
        f"Referral: {user['referrals']}\n\n"
        f"🔗 Link lu:\n{ref_link}"
    )

def help_command(update, context):
    update.message.reply_text(
        "📌 COMMAND:\n"
        "/start\n"
        "/reset\n"
        "/history\n"
        "/mode [santai/serius/toxic]\n"
        "/ref\n"
        "/top"
    )

def reset(update, context):
    uid = str(update.message.chat_id)
    chat_history.pop(uid, None)
    update.message.reply_text("♻️ Chat history direset!")

def history(update, context):
    uid = str(update.message.chat_id)
    hist = chat_history.get(uid, [])

    if not hist:
        update.message.reply_text("Belum ada history bro.")
        return

    text = "\n".join([f"{m['role']}: {m['content']}" for m in hist[-5:]])
    update.message.reply_text(f"🧾 Last chat:\n\n{text}")

def set_mode(update, context):
    uid = str(update.message.chat_id)
    try:
        mode = context.args[0]
        user_mode[uid] = mode
        update.message.reply_text(f"🎭 Mode diganti ke: {mode}")
    except:
        update.message.reply_text("Contoh: /mode santai")

def myref(update, context):
    uid = str(update.message.chat_id)
    user = get_user(uid)

    update.message.reply_text(
        f"👥 Referral: {user['referrals']}\n"
        f"⚡ Limit: {user['limit']}"
    )

def topref(update, context):
    sorted_users = sorted(db.items(), key=lambda x: x[1]["referrals"], reverse=True)

    text = "🏆 TOP REFERRAL:\n\n"
    for i, (uid, data) in enumerate(sorted_users[:5], start=1):
        text += f"{i}. {uid} → {data['referrals']} orang\n"

    update.message.reply_text(text)

# ===== CHAT =====
def chat(update, context):
    uid = str(update.message.chat_id)
    user_text = update.message.text
    user = get_user(uid)

    try:
        context.bot.send_chat_action(chat_id=int(uid), action=ChatAction.TYPING)
        time.sleep(1)

        # LIMIT SYSTEM
        if user["limit"] <= 0:
            update.message.reply_text("🚫 Limit habis. Cari referral bro 😎")
            return

        user["limit"] -= 1
        save_data(db)

        # SIMPAN NAMA
        if "nama aku" in user_text.lower():
            name = user_text.split("nama aku")[-1].strip()
            user["name"] = name
            save_data(db)
            update.message.reply_text(f"Siap {name}! gue inget 😎")
            return

        name = user.get("name", "bro")
        mode = user_mode.get(uid, "santai")

        # MODE STYLE
        if mode == "toxic":
            style = "Jawab sarkas, nyolot, tapi lucu."
        elif mode == "serius":
            style = "Jawab serius, jelas, informatif."
        else:
            style = "Jawab santai, gaul."

        # HISTORY
        if uid not in chat_history:
            chat_history[uid] = []

        chat_history[uid].append({"role": "user", "content": user_text})
        chat_history[uid] = chat_history[uid][-10:]

        messages = [
            {
                "role": "system",
                "content": f"""
Lu adalah MOMON.AI.
Panggil user: {name}.
{style}
Jawaban jangan kepanjangan.
"""
            }
        ] + chat_history[uid]

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile"
        )

        reply = response.choices[0].message.content

        chat_history[uid].append({"role": "assistant", "content": reply})

        update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"ERROR: {e}")
        update.message.reply_text("⚠️ Error bro, coba lagi nanti.")

# ===== MAIN =====
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(CommandHandler("mode", set_mode))
    dp.add_handler(CommandHandler("ref", myref))
    dp.add_handler(CommandHandler("top", topref))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    print("🚀 BOT MOMON AI FULL FITUR NYALA...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
