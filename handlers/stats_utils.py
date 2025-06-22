from services.db import get_user_stats, get_language
from services.translations import tr
from datetime import datetime

async def send_stats(chat_id: int, bot):
    stats, start_date = get_user_stats(chat_id)
    if not stats:
        return

    today = datetime.utcnow().strftime("%d.%m.%Y")
    start_str = start_date.strftime("%d.%m.%Y") if start_date else "?"

    period_line = f"🗓️ {tr(chat_id, 'period')}: {start_str} — {today}"
    title = tr(chat_id, "group_stats").capitalize()

    text = f"{title}\n{period_line}\n\n"
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['fap'] + x[1]['poop'], reverse=True)

    for user_display, data in sorted_stats:
        faps = data['fap']
        poops = data['poop']
        kd = round(faps / poops, 2) if poops != 0 else "∞"
        text += f"{user_display} — ✊ {faps}, 💩 {poops}, КД: {kd}\n"

    await bot.send_message(chat_id, text)
