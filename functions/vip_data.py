import sqlite3

DB_NAME = "vip_data.db"

def init_vip_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS vip_users (username TEXT PRIMARY KEY)")

def add_vip(username):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT OR IGNORE INTO vip_users (username) VALUES (?)", (username,))

def remove_vip(username):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM vip_users WHERE username = ?", (username,))

def is_vip(username):
    if username.lower() == "raybm":
        return True
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute("SELECT 1 FROM vip_users WHERE username = ?", (username,))
        return cur.fetchone() is not None

def get_all_vips():
    with sqlite3.connect(DB_NAME) as conn:
        return [row[0] for row in conn.execute("SELECT username FROM vip_users")]
