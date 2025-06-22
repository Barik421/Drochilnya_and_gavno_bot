from telegram import Update, Bot
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from services.db import connect, get_language, get_report_period, get_user_stats
from services.translations import tr
from services.db import get_report_period
from scheduler import send_winner_announcement

def calculate_period_start(period: str) -> datetime:
    now = datetime.utcnow()
    if period == "week":
        return now - timedelta(days=7)
    elif period == "month":
        return now - timedelta(days=30)
    elif period == "year":
        return now - timedelta(days=365)
    else:
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

def get_filtered_stats(chat_id: int, since: datetime):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT a.user_id, a.action_type, COUNT(*), u.name, u.allow_name
            FROM actions a
            LEFT JOIN users u ON a.user_id = u.user_id AND a.chat_id = u.chat_id
            WHERE a.chat_id = ? AND timestamp >= ?
            GROUP BY a.user_id, a.action_type
        ''', (chat_id, since.isoformat()))
        rows = cur.fetchall()

    stats = {}
    for user_id, action_type, count, name, allow_name in rows:
        display_name = name if allow_name and name else str(user_id)
        if display_name not in stats:
            stats[display_name] = {"fap": 0, "poop": 0}
        stats[display_name][action_type] = count

    return stats



async def handle_allstats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)
    stats, start_date = get_user_stats(chat_id)

    if not stats:
        await update.message.reply_text(tr(chat_id, "no_data"))
        return

    today = datetime.utcnow().strftime("%d.%m.%Y")
    start_str = start_date.strftime("%d.%m.%Y") if start_date else "?"
    period_line = f"🗓️ {tr(chat_id, 'period')}: {start_str} — {today}"
    title = tr(chat_id, "full_stats_title")

    text = f"{title}\n{period_line}\n\n"
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['fap'] + x[1]['poop'], reverse=True)

    for user, data in sorted_stats:
        faps = data['fap']
        poops = data['poop']
        kd = round(faps / poops, 2) if poops != 0 else "∞"
        text += f"👤 {user} — ✊ {faps}, 💩 {poops}, КД: {kd}\n"

    await update.message.reply_text(text)



async def handle_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    period = get_report_period(chat_id)
    stats, _ = get_user_stats(chat_id, period=period)

    if not stats:
        await update.message.reply_text(tr(chat_id, "no_data"))
        return

    # Сортуємо по сумі всіх дій
    sorted_stats = sorted(
        stats.items(),
        key=lambda x: x[1]['fap'] + x[1]['poop'],
        reverse=True
    )

    period_text = {
        "week": "за тиждень" if lang == "uk" else "this week",
        "month": "за місяць" if lang == "uk" else "this month",
        "year": "за рік" if lang == "uk" else "this year"
    }.get(period, "")

    title = {
        "uk": f"Топ користувачів {period_text}",
        "en": f"Top users {period_text}"
    }.get(lang, "Top")

    text = f"🏆 {title}\n\n"
    for i, (user_display, data) in enumerate(sorted_stats[:10], start=1):
        faps = data['fap']
        poops = data['poop']
        text += f"{i}. {user_display} — ✊ {faps}, 💩 {poops}\n"

    await update.message.reply_text(text)



async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    period = get_report_period(chat_id)
    stats, start_date = get_user_stats(chat_id, period=period)

    if not stats:
        await update.message.reply_text(tr(chat_id, "no_data"))
        return

    text = format_stats_text(chat_id, stats, start_date, period)
    await update.message.reply_text(text) 


def format_stats_text(chat_id, stats, start_date=None, period=None):
    lang = get_language(chat_id)

    title = "📊 Статистика" if lang == "uk" else "📊 Stats"
    today = datetime.utcnow().strftime("%d.%m.%Y")
    start_str = start_date.strftime("%d.%m.%Y") if start_date else "?"

    if period == "week":
        period_display = "🗓️ За тиждень" if lang == "uk" else "🗓️ Weekly"
    elif period == "month":
        period_display = "🗓️ За місяць" if lang == "uk" else "🗓️ Monthly"
    elif period == "year":
        period_display = "🗓️ За рік" if lang == "uk" else "🗓️ Yearly"
    else:
        period_display = f"🗓️ {tr(chat_id, 'period')}: {start_str} — {today}"

    text = f"{title}\n{period_display}\n\n"

    sorted_stats = sorted(stats.items(), key=lambda x: (x[1]['fap'] + x[1]['poop']), reverse=True)
    for user_id, data in sorted_stats:
        faps = data['fap']
        poops = data['poop']
        kd = round(faps / poops, 2) if poops != 0 else "∞"
        text += f"👤 {user_id} — ✊ {faps}, 💩 {poops}, КД: {kd}\n"

    return text



def calculate_period_start(period: str) -> datetime:
    now = datetime.utcnow()
    if period == "week":
        return now - timedelta(days=7)
    elif period == "month":
        return now - timedelta(days=30)
    elif period == "year":
        return now - timedelta(days=365)
    else:
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

def get_filtered_stats(chat_id: int, since: datetime):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT a.user_id, a.action_type, COUNT(*), u.name, u.allow_name
            FROM actions a
            LEFT JOIN users u ON a.user_id = u.user_id AND a.chat_id = u.chat_id
            WHERE a.chat_id = ? AND timestamp >= ?
            GROUP BY a.user_id, a.action_type
        ''', (chat_id, since.isoformat()))
        rows = cur.fetchall()

    stats = {}
    for user_id, action_type, count, name, allow_name in rows:
        display_name = name if allow_name and name else str(user_id)
        if display_name not in stats:
            stats[display_name] = {"fap": 0, "poop": 0}
        stats[display_name][action_type] = count

    return stats