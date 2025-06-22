from telegram import Update
from telegram.ext import ContextTypes

async def handle_misha_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.text and "міша" in message.text.lower():
        await message.reply_text("Жук")