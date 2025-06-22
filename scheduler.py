import datetime
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from services.db import get_all_chat_ids, get_report_period, get_user_stats, get_language
from handlers.stats import send_stats
from services.translations import tr

def start_scheduler(bot):
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=lambda: asyncio.run(check_and_send_reports(bot)),
        trigger=CronTrigger(hour=10, minute=0),
        timezone="UTC"
    )

    scheduler.start()

async def check_and_send_reports(bot):
    now = datetime.datetime.utcnow()
    weekday = now.weekday()
    day = now.day
    month = now.month

    chat_ids = get_all_chat_ids()
    for chat_id in chat_ids:
        period = get_report_period(chat_id)

        # Надсилання звіту за обраним періодом
        if (period == 'week' and weekday == 6) or \
           (period == 'month' and day == 1) or \
           (period == 'year' and day == 31 and month == 12):
            await send_stats(chat_id, bot)

        # 31 грудня — надсилання переможця
        if day == 31 and month == 12:
            await send_winner_announcement(chat_id, bot)

async def send_winner_announcement(chat_id: int, bot):
    stats, _ = get_user_stats(chat_id)
    if not stats:
        return

    # Знаходимо переможця за найбільшою сумою фапів і какань
    max_score = 0
    winners = []

    for user_id, data in stats.items():
        total = data['fap'] + data['poop']
        if total > max_score:
            max_score = total
            winners = [(user_id, data)]
        elif total == max_score:
            winners.append((user_id, data))

    lang = get_language(chat_id)
    title = (
        "🎉 Вітаю! Переможцем 2025 року по каканню й дрочінню стає:"
        if lang == "uk"
        else "🎉 Congratulations! The 2025 Champion of Pooping and Fapping is:"
    )

    message = f"{title}\n"
    for user_id, data in winners:
        faps = data["fap"]
        poops = data["poop"]
        kd = round(faps / poops, 2) if poops != 0 else "∞"
        message += f"👤 {user_id} — ✊ {faps}, 💩 {poops}, КД: {kd}\n"

    await bot.send_message(chat_id, message)
