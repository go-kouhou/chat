import sqlite3
from datetime import datetime

DB_PATH = 'chat_history.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id TEXT,
        user TEXT,
        message TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

# メッセージ保存

def save_message(room_id: str, user: str, message: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (room_id, user, message, timestamp) VALUES (?, ?, ?, ?)',
              (room_id, user, message, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

# 履歴取得

def get_messages(room_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user, message, timestamp FROM messages WHERE room_id=? ORDER BY id ASC', (room_id,))
    rows = c.fetchall()
    conn.close()
    return [ {'user': r[0], 'message': r[1], 'timestamp': r[2]} for r in rows ]

init_db()
