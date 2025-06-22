from telegram import Update
from telegram.ext import ContextTypes
from services.db import get_language

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    if lang == "uk":
        text = (
            "ℹ️ <b>Допомога</b>\n\n"
            "Цей бот дозволяє рахувати кількість дій:\n"
            "✊ — дрочіння (/fap)\n"
            "💩 — какання (/poop)\n\n"
            "<b>📊 Команди статистики:</b>\n"
            "/stats — статистика за період, вибраний у /settings\n"
            "/allstats — повна статистика з першого дня активності\n"
            "/top — топ користувачів за рік\n\n"
            "<b>⚙️ Інше:</b>\n"
            "/settings — вибір періоду (щотижня, щомісяця, щороку)\n"
            "/lang — зміна мови\n"
            "/reset — обнулити тільки вашу статистику\n"
            "/help — список доступних команд\n\n"
            "🥇 31 грудня бот автоматично оголошує переможця за рік\n\n"
            "❗ Обмеження:\n"
            "• Не більше 6 записів на день\n"
            
        )
    else:
        text = (
            "ℹ️ <b>Help</b>\n\n"
            "This bot counts actions:\n"
            "✊ — fapping (/fap)\n"
            "💩 — pooping (/poop)\n\n"
            "<b>📊 Stats commands:</b>\n"
            "/stats — statistics for the selected period in /settings\n"
            "/allstats — full statistics since first activity\n"
            "/top — top users of the year\n\n"
            "<b>⚙️ Other:</b>\n"
            "/settings — choose period (weekly, monthly, yearly)\n"
            "/lang — change language\n"
            "/reset — reset your personal stats\n"
            "/help — list of available commands\n\n"
            "🥇 On December 31, the bot will announce the yearly winner\n\n"
            "❗ Limits:\n"
            "• Max 6 actions per day\n"
            
        )

    await update.message.reply_text(text, parse_mode="HTML")