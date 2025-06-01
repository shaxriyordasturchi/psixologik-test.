import sqlite3
from datetime import datetime, timedelta
import random

# Ma'lumotlar bazasi yaratish
conn = sqlite3.connect("telekom.db")
c = conn.cursor()

# 1. Abonentlar jadvali
c.execute("DROP TABLE IF EXISTS abonentlar")
c.execute("""
CREATE TABLE abonentlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ism TEXT,
    familiya TEXT,
    raqam TEXT UNIQUE,
    tarif_rejasi TEXT,
    hudud TEXT,
    faollashtirilgan DATE
)
""")

# 2. Chiquvchi qo‘ng‘iroqlar jadvali
c.execute("DROP TABLE IF EXISTS chiquvchi_qongiroqlar")
c.execute("""
CREATE TABLE chiquvchi_qongiroqlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    abonent_id INTEGER,
    sana DATE,
    davomiylik INTEGER,
    FOREIGN KEY (abonent_id) REFERENCES abonentlar(id)
)
""")

# Test abonentlar ro'yxati
abonentlar = [
    ("Ali", "Karimov", "998901111111", "Smart 10", "Toshkent", "2024-05-01"),
    ("Dilnoza", "Olimova", "998901111112", "Ultra", "Farg'ona", "2024-04-15"),
    ("Sardor", "Rustamov", "998901111113", "Smart 10", "Andijon", "2024-05-10"),
    ("Zafar", "Yusupov", "998901111114", "Mini", "Samarqand", "2024-03-20"),
    ("Malika", "Nurmatova", "998901111115", "Smart 10", "Buxoro", "2024-05-25"),
    ("Javohir", "Qodirov", "998901111116", "Ultra", "Toshkent", "2024-05-03"),
    ("Aziza", "Solieva", "998901111117", "Mini", "Xorazm", "2024-04-28"),
    ("Bekzod", "Eshonov", "998901111118", "Smart 10", "Namangan", "2024-05-30"),
    ("Rayhon", "Usmonova", "998901111119", "Ultra", "Sirdaryo", "2024-05-31"),
    ("Otabek", "Ismoilov", "998901111120", "Mini", "Qashqadaryo", "2024-05-20"),
]

# Abonentlarni bazaga joylash
for a in abonentlar:
    c.execute("""
    INSERT INTO abonentlar (ism, familiya, raqam, tarif_rejasi, hudud, faollashtirilgan)
    VALUES (?, ?, ?, ?, ?, ?)
    """, a)

# Abonent IDlarini olish
c.execute("SELECT id FROM abonentlar")
abonent_idlar = [row[0] for row in c.fetchall()]

# Chiquvchi qo‘ng‘iroqlarni yaratish (tasodifiy)
for _ in range(30):
    abonent_id = random.choice(abonent_idlar)
    sana = datetime.today() - timedelta(days=random.randint(1, 60))
    davomiylik = random.randint(1, 300)  # soniyada
    c.execute("""
    INSERT INTO chiquvchi_qongiroqlar (abonent_id, sana, davomiylik)
    VALUES (?, ?, ?)
    """, (abonent_id, sana.date(), davomiylik))

# Saqlash va yopish
conn.commit()
conn.close()

print("✅ Ma'lumotlar bazasi tayyorlandi: telekom.db")
