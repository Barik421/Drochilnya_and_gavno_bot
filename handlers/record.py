from telegram import Update
from telegram.ext import ContextTypes
from services.db import add_action, connect
from datetime import datetime

LIMIT_PER_DAY = 6

def get_action_count(user_id: int, action_type: str, date: str):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT COUNT(*) FROM actions
            WHERE user_id = ? AND action_type = ? AND date(timestamp) = ?
        ''', (user_id, action_type, date))
        result = cur.fetchone()
        return result[0] if result else 0

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE, action_type: str):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    today = datetime.utcnow().date().isoformat()

    count = get_action_count(user_id, action_type, today)

    if count >= LIMIT_PER_DAY:
        await update.message.reply_text("🚫 Ліміт досягнуто! Не більше 6 разів на день 😉")
        return

    add_action(user_id, chat_id, action_type)
    emoji = "💩" if action_type == "poop" else "✊"
    await update.message.reply_text(f"{emoji} Записано! ({count + 1}/6)")

async def handle_fap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_action(update, context, "fap")

async def handle_poop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_action(update, context, "poop")
