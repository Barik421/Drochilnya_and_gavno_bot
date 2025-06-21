from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from services.db import set_language
from services.translations import tr



# Команда /lang — вибір мови
async def handle_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_uk')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(tr(chat_id, "lang_select"))

# Обробник натискань на кнопку
async def handle_lang_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    selected = query.data

    if selected == 'lang_uk':
        set_language(chat_id, 'uk')
        await query.edit_message_text("✅ Мову встановлено: 🇺🇦 Українська")
    elif selected == 'lang_en':
        set_language(chat_id, 'en')
        await query.edit_message_text("✅ Language set: 🇬🇧 English")


async def handle_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id  # 🔧 потрібний рядок
    keyboard = [
        [InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(tr(chat_id, "lang_select"), reply_markup=reply_markup)