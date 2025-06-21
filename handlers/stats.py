from telegram import Update
from telegram.ext import ContextTypes
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.db import connect
from datetime import datetime, timedelta
from services.translations import tr

def get_stats(user_id, chat_id, period):
    with connect() as conn:
        cur = conn.cursor()
        
        if period == "week":
            since = datetime.utcnow() - timedelta(days=7)
        elif period == "month":
            since = datetime.utcnow() - timedelta(days=30)
        elif period == "year":
            since = datetime.utcnow() - timedelta(days=365)
        else:
            since = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        cur.execute('''
            SELECT action_type, COUNT(*) FROM actions
            WHERE user_id = ? AND chat_id = ? AND timestamp >= ?
            GROUP BY action_type
        ''', (user_id, chat_id, since.isoformat()))
        
        result = {row[0]: row[1] for row in cur.fetchall()}
        return result

def get_group_stats(chat_id, period):
    with connect() as conn:
        cur = conn.cursor()

        if period == "week":
            since = datetime.utcnow() - timedelta(days=7)
        elif period == "month":
            since = datetime.utcnow() - timedelta(days=30)
        elif period == "year":
            since = datetime.utcnow() - timedelta(days=365)
        else:
            since = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        cur.execute('''
            SELECT user_id, action_type, COUNT(*) as count FROM actions
            WHERE chat_id = ? AND timestamp >= ?
            GROUP BY user_id, action_type
            ORDER BY count DESC
        ''', (chat_id, since.isoformat()))
        
        data = cur.fetchall()
        return data

from services.translations import tr

async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    args = context.args

    period = args[0].lower() if args else "today"
    if period not in ("today", "week", "month", "year"):
        period = "today"

    personal = get_stats(user_id, chat_id, period)
    group = get_group_stats(chat_id, period)

    faps = personal.get("fap", 0)
    poops = personal.get("poop", 0)
    kd = round(poops / faps, 2) if faps else "∞"

    # 🧠 Персональна статистика
    text = f"📊 <b>{tr(chat_id, 'your_stats', period=period)}:</b>\n"
    text += f"{tr(chat_id, 'fap')}: {faps}\n"
    text += f"{tr(chat_id, 'poop')}: {poops}\n"
    text += f"{tr(chat_id, 'kd')}: {kd}\n\n"

    # 🧠 Групова статистика
    text += f"👥 <b>{tr(chat_id, 'group_stats', period=period)}:</b>\n"
    summary = {}
    for uid, act, count in group:
        if uid not in summary:
            summary[uid] = {"fap": 0, "poop": 0}
        summary[uid][act] += count

    sorted_summary = sorted(summary.items(), key=lambda x: x[1]["poop"] + x[1]["fap"], reverse=True)
    for idx, (uid, actions) in enumerate(sorted_summary, 1):
        total = actions["fap"] + actions["poop"]
        text += f"{idx}. ID: <code>{uid}</code> — {total} {tr(chat_id, 'actions_total')} (✊ {actions['fap']}, 💩 {actions['poop']})\n"

    await update.message.reply_text(text, parse_mode="HTML")

