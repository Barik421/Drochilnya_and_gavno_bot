import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from handlers.record import handle_fap, handle_poop
from telegram.ext import CommandHandler

# Завантаження змінних із .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я твій бот 😎")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
    app.add_handler(CommandHandler("fap", handle_fap))
    app.add_handler(CommandHandler("poop", handle_poop))