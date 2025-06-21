from telegram import Update
from .db import connect

def update_user_info(update: Update):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Ставимо @ лише якщо username не None
    name = f"@{user.username}" if user.username else user.full_name

    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO users (user_id, chat_id, name, allow_name)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(user_id, chat_id) DO UPDATE SET name = excluded.name, allow_name = 1
        ''', (user.id, chat_id, name))
        conn.commit()