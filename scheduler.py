from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from services.db import connect
from telegram import Bot
import asyncio

bot = None  # Ми підв'яжемо об'єкт бота у main.py

def get_all_chats():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT chat_id FROM settings")
        return [row[0] for row in cur.fetchall()]

def get_winner(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, username, COUNT(*) as total
            FROM actions
            WHERE chat_id = ?
            GROUP BY user_id, username
            ORDER BY total DESC
            LIMIT 1
        """, (chat_id,))
        return cur.fetchone()

async def send_yearly_report():
    today = datetime.now()
    if today.month == 12 and today.day == 31:
        print("🎉 Надсилаємо річні звіти...")
        for chat_id in get_all_chats():
            winner = get_winner(chat_id)
            if winner:
                user_id, username, total = winner
                text = f"🎉 Переможець року по дрочильні і сранню в цьому чаті: @{username or 'невідомий'}!\nЗагалом дій: {total}\nВітаємо! 🥳"
            else:
                text = "🤷 Немає активності цього року. Хто ж буде першим у новому?"

            try:
                await bot.send_message(chat_id, tr(chat_id, "winner", username=username, count=total))
            except Exception as e:
                print(f"⚠️ Не вдалося надіслати повідомлення в {chat_id}: {e}")

def start_scheduler(app_bot):
    global bot
    bot = app_bot

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.create_task(send_yearly_report()), 'cron', hour=20)
    scheduler.start()
