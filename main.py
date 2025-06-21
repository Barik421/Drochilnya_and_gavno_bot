import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
)

# Імпорти власних модулів
from services.db import init_db
from services.translations import tr
from handlers.record import handle_fap, handle_poop
from handlers.stats import handle_stats
from handlers.lang import handle_lang, handle_lang_choice
from handlers.reset import handle_reset, handle_reset_callback
from handlers.settings import handle_settings, handle_period_selection
from scheduler import start_scheduler
from handlers.stats import handle_stats, send_stats, handle_report_test, handle_winner_test


# Налаштування логування
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR
)

# Завантаження токена з .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(tr(chat_id, "start"))

# Основна функція запуску бота
async def main():
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команди
    commands = [
        BotCommand("start", "Запуск бота"),
        BotCommand("stats", "📊 Статистика"),
        BotCommand("settings", "🔧 Налаштування звітів"),
        BotCommand("lang", "🌐 Змінити мову"),
        BotCommand("reset", "♻️ Обнулити статистику"),
        BotCommand("fap", "✊ Додати дрочіння"),
        BotCommand("poop", "💩 Додати какання"),
        BotCommand("reporttest", "🧪 Тест надсилання статистики"),
        BotCommand("winner", "🏆 Тест переможця року")
    ]
    await app.bot.set_my_commands(commands)

    # Обробники команд
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
    app.add_handler(CommandHandler("reporttest", handle_report_test))
    app.add_handler(CommandHandler("winner", handle_winner_test))

    # ✅ Обробник помилок
    from telegram.error import TelegramError

    async def error_handler(update, context):
        print(f"❌ Помилка: {context.error}")

    app.add_error_handler(error_handler)

    # ✅ Планувальник
    start_scheduler(app.bot)

    # ✅ Запуск бота
    await app.run_polling()


# Запуск через asyncio
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())

