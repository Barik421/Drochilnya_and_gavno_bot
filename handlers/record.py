from telegram import Update
from telegram.ext import ContextTypes
from services.db import add_action, get_language
from services.translations import tr
from datetime import datetime
from services.db import connect
from services.user_utils import update_user_info

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

    lang = get_language(chat_id)

    if count >= LIMIT_PER_DAY:
        await update.message.reply_text(tr(chat_id, "limit_reached"))
        return

    add_action(user_id, chat_id, action_type)

    if action_type == "poop":
        emoji = "💩"
    else:
        emoji = "✊"

    await update.message.reply_text(
    tr(chat_id, "action_recorded", emoji=emoji, count=count + 1, limit=LIMIT_PER_DAY)
)

async def handle_fap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_user_info(update)

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    add_action(user_id, chat_id, "fap")

    await update.message.reply_text(tr(chat_id, "fap_recorded"))

async def handle_poop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_user_info(update)

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    add_action(user_id, chat_id, "poop")

    await update.message.reply_text(tr(chat_id, "poop_recorded"))
    
print(update_user_info)