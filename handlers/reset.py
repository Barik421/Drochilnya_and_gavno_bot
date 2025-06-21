from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.db import delete_user_data

# Команда /reset — запит підтвердження
async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("❗ Скидання статистики в групі поки недоступне. Скоро додамо підтримку голосування!")
        return

    keyboard = [
        [
            InlineKeyboardButton("✅ Так", callback_data="confirm_reset"),
            InlineKeyboardButton("❌ Ні", callback_data="cancel_reset"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚠️ Ти впевнений, що хочеш обнулити ВСЮ свою статистику?", reply_markup=reply_markup)

# Обробка кнопок підтвердження
async def handle_reset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if query.data == "confirm_reset":
        delete_user_data(chat_id, user_id)
        await query.edit_message_text("✅ Вся твоя статистика обнулена.")
    else:
        await query.edit_message_text("❌ Скасовано. Дані залишились без змін.")
