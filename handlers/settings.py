from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.db import set_report_period, get_report_period
from services.translations import tr

# Команда /settings — показ кнопок вибору періоду
async def handle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    keyboard = [
        [
            InlineKeyboardButton(tr(chat_id, "weekly"), callback_data="report_week"),
            InlineKeyboardButton(tr(chat_id, "monthly"), callback_data="report_month"),
            InlineKeyboardButton(tr(chat_id, "yearly"), callback_data="report_year"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    current = get_report_period(chat_id)
    mapping = {
        "week": tr(chat_id, "weekly"),
        "month": tr(chat_id, "monthly"),
        "year": tr(chat_id, "yearly")
    }

    await update.message.reply_text(
        tr(chat_id, "settings_prompt", current=mapping.get(current, tr(chat_id, "yearly"))),
        reply_markup=reply_markup
    )

# Обробка вибору
async def handle_period_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    data = query.data

    mapping = {
        "report_week": "week",
        "report_month": "month",
        "report_year": "year"
    }

    if data in mapping:
        set_report_period(chat_id, mapping[data])
        await query.edit_message_text(tr(chat_id, "period_saved"))
