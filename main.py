from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from services.db import init_db
from handlers.record import handle_fap, handle_poop
from handlers.stats import handle_stats
from dotenv import load_dotenv
import os
from handlers.lang import handle_lang, handle_lang_choice
from telegram.ext import CallbackQueryHandler
from handlers.reset import handle_reset, handle_reset_callback
from handlers.settings import handle_settings, handle_period_selection
from telegram.ext import CallbackQueryHandler, CommandHandler
from scheduler import start_scheduler
from telegram import BotCommand


# Завантаження токена з .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот Дрочильня 💩✊\nВикористовуй /fap або /poop для запису.\n/stats — щоб побачити статистику!")

# Запуск бота
if __name__ == '__main__':
    import asyncio

    async def main():
        init_db()

        app = ApplicationBuilder().token(BOT_TOKEN).build()

        commands = [
            BotCommand("start", "Запуск бота"),
            BotCommand("stats", "Статистика"),
            BotCommand("settings", "Налаштування звітів"),
            BotCommand("lang", "Змінити мову"),
            BotCommand("reset", "Обнулити статистику")
        ]
        await app.bot.set_my_commands(commands)

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("fap", handle_fap))
        app.add_handler(CommandHandler("poop", handle_poop))
        app.add_handler(CommandHandler("stats", handle_stats))
        app.add_handler(CommandHandler("lang", handle_lang))
        app.add_handler(CallbackQueryHandler(handle_lang_choice, pattern="^lang_"))
        app.add_handler(CommandHandler("reset", handle_reset))
        app.add_handler(CallbackQueryHandler(handle_reset_callback, pattern="^confirm_reset|cancel_reset$"))
        app.add_handler(CommandHandler("settings", handle_settings))
        app.add_handler(CallbackQueryHandler(handle_period_selection, pattern="^report_"))

        start_scheduler(app.bot)

        await app.run_polling()

    asyncio.run(main())


import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR
)
start_scheduler(app.bot)
app.run_polling()
