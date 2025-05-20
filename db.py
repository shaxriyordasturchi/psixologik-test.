import sqlite3
import pandas as pd

DB_NAME = "results.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            age INTEGER,
            gender TEXT,
            region TEXT,
            a_count INTEGER,
            b_count INTEGER,
            c_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_result(name, surname, age, gender, region, a, b, c):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (name, surname, age, gender, region, a_count, b_count, c_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, surname, age, gender, region, a, b, c))
    conn.commit()
    conn.close()

def get_all_results():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM results", conn)
    conn.close()
    return df
