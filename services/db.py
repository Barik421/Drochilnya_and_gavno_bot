import sqlite3
from datetime import datetime

# Підключення до бази
def connect():
    return sqlite3.connect("data.db")

# Ініціалізація таблиць
def init_db():
    with connect() as conn:
        cur = conn.cursor()

        # Таблиця дій (fap/poop)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                action_type TEXT,
                timestamp TEXT
            )
        ''')

        # Таблиця налаштувань (мова)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                chat_id INTEGER PRIMARY KEY,
                lang TEXT DEFAULT 'uk'
            )
        ''')

        conn.commit()

# Додавання дії користувача
def add_action(user_id: int, chat_id: int, action_type: str):
    timestamp = datetime.utcnow().isoformat()
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO actions (user_id, chat_id, action_type, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, chat_id, action_type, timestamp))
        conn.commit()

# Встановлення мови для чату
def set_language(chat_id: int, lang: str):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO settings (chat_id, lang)
            VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET lang=excluded.lang
        ''', (chat_id, lang))
        conn.commit()

# Отримання мови для чату
def get_language(chat_id: int):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT lang FROM settings WHERE chat_id = ?', (chat_id,))
        row = cur.fetchone()
        return row[0] if row else 'uk'

        
# Скидання статисти користувача
def delete_user_data(chat_id: int, user_id: int):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            DELETE FROM actions
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        conn.commit()
