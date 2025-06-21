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
    }
}




from services.db import get_lang

def tr(chat_id, key, **kwargs):
    lang = get_lang(chat_id)
    text = translations.get(key, {}).get(lang, "")
    return text.format(**kwargs)