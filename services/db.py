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

        cur.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            chat_id INTEGER PRIMARY KEY,
            lang TEXT DEFAULT 'uk',
            report_period TEXT DEFAULT 'year'
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


def get_user_stats(chat_id: int) -> tuple:
    with connect() as conn:
        cur = conn.cursor()

        # Статистика по користувачах
        cur.execute('''
            SELECT user_id, action_type, COUNT(*) FROM actions
            WHERE chat_id = ?
            GROUP BY user_id, action_type
        ''', (chat_id,))
        rows = cur.fetchall()

        # Дата найпершої дії в цьому чаті
        cur.execute('''
            SELECT MIN(timestamp) FROM actions WHERE chat_id = ?
        ''', (chat_id,))
        start_row = cur.fetchone()

    stats = {}
    for user_id, action_type, count in rows:
        if user_id not in stats:
            stats[user_id] = {"fap": 0, "poop": 0}
        stats[user_id][action_type] = count

    # Конвертуємо ISO дату
    start_date = None
    if start_row and start_row[0]:
        from datetime import datetime
        start_date = datetime.fromisoformat(start_row[0])

    return stats, start_date

       