translations = {
    "lang_select": {
        "uk": "🌐 Обери мову:",
        "en": "🌐 Choose your language:"
    },
    "lang_saved": {
        "uk": "✅ Мову збережено!",
        "en": "✅ Language saved!"
    },
    "settings_prompt": {
        "uk": "🔧 Обери як часто отримувати статистику:\n\nПоточне значення: {value}",
        "en": "🔧 Choose how often to receive stats:\n\nCurrent: {value}"
    },
    "period_saved": {
        "uk": "✅ Налаштування збережено.",
        "en": "✅ Settings saved."
    },
    "winner": {
        "uk": "🎉 Переможець року у цьому чаті: @{username}!\nЗагалом дій: {count}\nВітаємо! 🥳",
        "en": "🎉 Yearly winner in this chat: @{username}!\nTotal actions: {count}\nCongratulations! 🥳"
    },
    "no_activity": {
        "uk": "🤷 Немає активності цього року. Хто ж буде першим у новому?",
        "en": "🤷 No activity this year. Who will start the next one?"
    },
    "your_stats": {
        "uk": "Твоя статистика ({period})",
        "en": "Your statistics ({period})"
    },
    "group_stats": {
        "uk": "Загальна статистика ({period})",
        "en": "Group statistics ({period})"
    },
    "fap": {
        "uk": "✊ Дрочив",
        "en": "✊ Fapped"
    },
    "poop": {
        "uk": "💩 Какав",
        "en": "💩 Pooped"
    },
    "kd": {
        "uk": "КД",
        "en": "K/D"
    },
    "actions_total": {
        "uk": "дій",
        "en": "actions"
    },
    "start": {
        "uk": "Привіт! Я бот Дрочильня 👋\n\nНадішли /fap або /poop, щоб записати дію.\n/stats — щоб переглянути статистику.",
        "en": "Hi! I am Drochilnya bot 👋\n\nSend /fap or /poop to record an action.\n/stats — to view your stats."
    },
    "limit_reached": {
        "uk": "⛔ Ліміт досягнуто! Не більше 6 разів на день 😬",
        "en": "⛔ Limit reached! No more than 6 times a day 😬"
    },
    "action_recorded": {
        "uk": "{emoji} Записано! ({count} / {limit})",
        "en": "{emoji} Recorded! ({count} / {limit})"
    },

    "reset_prompt": {"uk": "🔁 Ви дійсно хочете обнулити статистику?", "en": "🔁 Do you really want to reset stats?"},
    "confirm_reset": {"uk": "✅ Так, обнулити", "en": "✅ Yes, reset"},
    "cancel_reset": {"uk": "❌ Ні, скасувати", "en": "❌ No, cancel"},
    "reset_done": {"uk": "✅ Статистика обнулена!", "en": "✅ Stats have been reset!"},
    "reset_canceled": {"uk": "❌ Скасовано.", "en": "❌ Cancelled."},

    "period": {
    "uk": "Період",
    "en": "Period"
        },

        "period": {
        "uk": "Період",
        "en": "Period"
    },

        "fap_recorded": {
        "uk": "✊ Дрочіння зараховано!",
        "en": "✊ Fap recorded!"
    },
    "poop_recorded": {
        "uk": "💩 Какання зараховано!",
        "en": "💩 Poop recorded!"
    },

    "cooldown_fap": {
    "uk": "⏳ Почекай трохи перед наступним дрочінням.",
    "en": "⏳ Wait a bit before fapping again."
    },
    "cooldown_poop": {
        "uk": "⏳ Почекай трохи перед наступним каканням.",
        "en": "⏳ Wait a bit before pooping again."
    },
    "top_title": {
    "uk": "Топ користувачів:",
    "en": "Top users:"
    },
    "actions_total": {
        "uk": "дій",
        "en": "actions"
    },
    "no_data": {
        "uk": "🤷 Немає даних для статистики.",
        "en": "🤷 No data for statistics."
    }
                
}



from services.db import get_lang

def tr(chat_id, key, **kwargs):
    lang = get_lang(chat_id)
    text = translations.get(key, {}).get(lang, "")
    return text.format(**kwargs)