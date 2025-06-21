from telegram import Update
from telegram.ext import ContextTypes
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.db import connect
from datetime import datetime, timedelta
from services.translations import tr
from telegram import Update
from telegram.ext import ContextTypes
from services.db import get_language, get_user_stats
from services.translations import tr
from telegram import Bot

async def handle_report_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await send_stats(chat_id, context.bot)

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
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)
    stats, start_date = get_user_stats(chat_id)

    if not stats:
        await update.message.reply_text(tr(chat_id, "no_data"))
        return

    from datetime import datetime
    today = datetime.utcnow().strftime("%d.%m.%Y")
    start_str = start_date.strftime("%d.%m.%Y") if start_date else "?"

    period_line = f"🗓️ {tr(chat_id, 'period')}: {start_str} — {today}"
    title = "📊 Статистика" if lang == "uk" else "📊 Stats"

    text = f"{title}\n{period_line}\n\n"
    sorted_stats = sorted(stats.items(), key=lambda x: (x[1]['fap'] + x[1]['poop']), reverse=True)

    for user_id, data in sorted_stats:
        faps = data['fap']
        poops = data['poop']
        kd = round(faps / poops, 2) if poops != 0 else "∞"

        text += f"👤 ID {user_id} — ✊ {faps}, 💩 {poops}, КД: {kd}\n"

    await update.message.reply_text(text)


# Статистика таймерів

from datetime import datetime
from services.db import get_language, get_user_stats
from telegram import Bot
from services.translations import tr

async def send_stats(chat_id: int, bot: Bot = None):
    if not bot:
        print("❌ Помилка: не передано bot для send_stats")
        return

    lang = get_language(chat_id)
    stats, start_date = get_user_stats(chat_id)

    if not stats:
        await bot.send_message(chat_id, tr(chat_id, "no_data"))
        return

    today = datetime.utcnow().strftime("%d.%m.%Y")
    start_str = start_date.strftime("%d.%m.%Y") if start_date else "?"

    period_line = f"🗓️ {tr(chat_id, 'period')}: {start_str} — {today}"
    title = "📊 Статистика" if lang == "uk" else "📊 Stats"

    text = f"{title}\n{period_line}\n\n"
    sorted_stats = sorted(stats.items(), key=lambda x: (x[1]['fap'] + x[1]['poop']), reverse=True)

    for user_id, data in sorted_stats:
        faps = data['fap']
        poops = data['poop']
        kd = round(faps / poops, 2) if poops != 0 else "∞"

        text += f"👤 ID {user_id} — ✊ {faps}, 💩 {poops}, КД: {kd}\n"

    await bot.send_message(chat_id, text)


