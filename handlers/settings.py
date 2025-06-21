from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.db import set_report_period, get_report_period

# Команда /settings — показ кнопок вибору періоду
async def handle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Щотижня", callback_data="report_week")],
        [InlineKeyboardButton("🗓 Щомісяця", callback_data="report_month")],
        [InlineKeyboardButton("📆 Щороку", callback_data="report_year")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    current = get_report_period(update.effective_chat.id)
    mapping = {"week": "📅 Щотижня", "month": "🗓 Щомісяця", "year": "📆 Щороку"}

    await update.message.reply_text(
        f"🔧 Обери як часто отримувати статистику:\n\nПоточне значення: {mapping.get(current, '📆 Щороку')}",
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
        await query.edit_message_text("✅ Налаштування збережено.")
