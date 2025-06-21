from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.db import clear_user_stats, get_language
from services.translations import tr

async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(tr(chat_id, "confirm_reset"), callback_data="confirm_reset")],
        [InlineKeyboardButton(tr(chat_id, "cancel_reset"), callback_data="cancel_reset")]
    ])
    await update.message.reply_text(tr(chat_id, "reset_prompt"), reply_markup=keyboard)

async def handle_reset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    lang = get_language(chat_id)

    if query.data == "confirm_reset":
        clear_user_stats(user_id)
        await query.edit_message_text(tr(chat_id, "reset_done"))
    else:
        await query.edit_message_text(tr(chat_id, "reset_canceled"))
