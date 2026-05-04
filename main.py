import os
import logging
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from groq import Groq

# ===== CONFIG =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(level=logging.INFO)

# ===== ADMIN =====
ADMIN_ID = "8385676898"

# ===== DATABASE SEMENTARA =====
user_memory = {}
chat_history = {}
user_mode = {}

referrals = {}
user_ref = {}
user_limit = {}
user_premium = {}

LIMIT_FREE = 10
REF_PREMIUM = 3

# ===== COMMANDS =====
def start(update, context):
    uid = str(update.message.chat_id)

    # admin auto premium
    if uid == ADMIN_ID:
        user_premium[uid] = True

    # referral
    if context.args:
        ref_id = context.args[0]

        if ref_id != uid and uid not in user_ref:
            user_ref[uid] = ref_id

            referrals[ref_id] = referrals.get(ref_id, 0) + 1

    update.message.reply_text(
        "🔥 MOMON.AI aktif bro!\n\n"
        "💬 Chat bebas\n"
        "🎁 Referral = unlock premium\n\n"
        "Ketik /help"
    )

def help_command(update, context):
    update.message.reply_text(
        "/start\n/help\n/reset\n/history\n/mode santai\n/ref\n/status\n/addlimit"
    )

def reset(update, context):
    uid = update.message.chat_id
    user_memory.pop(uid, None)
    chat_history.pop(uid, None)
    update.message.reply_text("♻️ Memory direset!")

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

def ref(update, context):
    uid = str(update.message.chat_id)

    total = referrals.get(uid, 0)
    link = f"https://t.me/{context.bot.username}?start={uid}"

    update.message.reply_text(
        f"👥 Referral: {total}\n\n🔗 {link}"
    )

def status(update, context):
    uid = str(update.message.chat_id)

    limit = user_limit.get(uid, 0)
    premium = user_premium.get(uid, False)

    update.message.reply_text(
        f"📊 Status:\n"
        f"Limit: {limit}/{LIMIT_FREE}\n"
        f"Premium: {'YES 🔥' if premium else 'NO'}"
    )

def addlimit(update, context):
    uid = str(update.message.chat_id)

    if uid != ADMIN_ID:
        update.message.reply_text("❌ Lu bukan admin")
        return

    user_limit.clear()
    update.message.reply_text("🔥 Semua limit direset!")

# ===== CHAT =====
def chat(update, context):
    uid = str(update.message.chat_id)
    user_text = update.message.text

    try:
        # admin bypass
        if uid == ADMIN_ID:
            user_premium[uid] = True

        if uid not in user_limit:
            user_limit[uid] = 0

        # limit check
        if not user_premium.get(uid, False):
            if user_limit[uid] >= LIMIT_FREE:
                update.message.reply_text(
                    "❌ Limit habis!\nCari referral bro 😎\n/ref"
                )
                return

        user_limit[uid] += 1

        # unlock premium dari referral
        if referrals.get(uid, 0) >= REF_PREMIUM:
            user_premium[uid] = True

        context.bot.send_chat_action(chat_id=uid, action=ChatAction.TYPING)
        time.sleep(1)

        # save nama
        if "nama aku" in user_text.lower():
            name = user_text.split("nama aku")[-1].strip()
            user_memory[uid] = name
            update.message.reply_text(f"Siap {name} 😎")
            return

        name = user_memory.get(uid, "bro")
        mode = user_mode.get(uid, "santai")

        if mode == "toxic":
            style = "Jawab sarkas, nyolot tapi lucu."
        elif mode == "serius":
            style = "Jawab serius dan jelas."
        else:
            style = "Jawab santai kayak temen."

        if uid not in chat_history:
            chat_history[uid] = []

        chat_history[uid].append({"role": "user", "content": user_text})
        chat_history[uid] = chat_history[uid][-10:]

        messages = [
            {
                "role": "system",
                "content": f"""
Lu MOMON.AI
Panggil user: {name}
{style}
Jawaban singkat.
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
    dp.add_handler(CommandHandler("ref", ref))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("addlimit", addlimit))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    print("🚀 MOMON AI ADMIN MODE ON 🔥")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
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
