import sqlite3

DB_NAME = "abonents.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS abonents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        chat_id INTEGER UNIQUE
    )
    """)
    conn.commit()
    conn.close()

def add_abonent(name: str, chat_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM abonents WHERE chat_id = ?", (chat_id,))
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute("INSERT INTO abonents (name, chat_id) VALUES (?, ?)", (name, chat_id))
    conn.commit()
    conn.close()
    return True

def get_all_abonents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, chat_id FROM abonents")
    results = cursor.fetchall()
    conn.close()
    return results

def get_abonent_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, chat_id FROM abonents WHERE name LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def remove_abonent(abonent_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM abonents WHERE id = ?", (abonent_id,))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes
