import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes


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

        cur.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            chat_id INTEGER PRIMARY KEY,
            lang TEXT DEFAULT 'uk',
            report_period TEXT DEFAULT 'year'
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            chat_id INTEGER,
            name TEXT,
            allow_name INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, chat_id)
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

# Таймери для статистики
def set_report_period(chat_id: int, period: str):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO settings (chat_id, report_period)
            VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET report_period=excluded.report_period
        ''', (chat_id, period))
        conn.commit()

def get_report_period(chat_id: int):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('SELECT report_period FROM settings WHERE chat_id = ?', (chat_id,))
        row = cur.fetchone()
        return row[0] if row else 'year'
    
def get_lang(chat_id: int):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT lang FROM settings WHERE chat_id = ?", (chat_id,))
        row = cur.fetchone()
        return row[0] if row else 'uk'
    
def clear_user_stats(user_id: int):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM actions WHERE user_id = ?', (user_id,))
        conn.commit()    


def get_user_stats(chat_id: int, period: str = None) -> tuple:
    with connect() as conn:
        cur = conn.cursor()

        cur.execute('''
            SELECT a.user_id, a.action_type, COUNT(*), u.name, u.allow_name
            FROM actions a
            LEFT JOIN users u ON a.user_id = u.user_id AND a.chat_id = u.chat_id
            WHERE a.chat_id = ?
            GROUP BY a.user_id, a.action_type
        ''', (chat_id,))
        rows = cur.fetchall()

        cur.execute('''
            SELECT MIN(timestamp) FROM actions WHERE chat_id = ?
        ''', (chat_id,))
        start_row = cur.fetchone()

    stats = {}
    for user_id, action_type, count, name, allow_name in rows:
        if allow_name and name:
            display_name = name
        else:
            display_name = f"{user_id}"

        if display_name not in stats:
            stats[display_name] = {"fap": 0, "poop": 0}
        stats[display_name][action_type] = count

    # Дата початку
    start_date = None
    if start_row and start_row[0]:
        from datetime import datetime
        start_date = datetime.fromisoformat(start_row[0])

    return stats, start_date

def get_all_chat_ids() -> list:
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT chat_id FROM actions")
        rows = cur.fetchall()
        return [row[0] for row in rows]       
    
