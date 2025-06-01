import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# Ma'lumotlar bazasiga ulanish
def get_connection():
    return sqlite3.connect("telekom.db", check_same_thread=False)

# So‘rov 1: Eng ko‘p qo‘ng‘iroq qilgan abonentlar
def top_caller():
    conn = get_connection()
    query = """
    SELECT a.ism, a.familiya, COUNT(q.id) AS qongiroqlar_soni
    FROM abonentlar a
    JOIN chiquvchi_qongiroqlar q ON a.id = q.abonent_id
    GROUP BY a.id
    ORDER BY qongiroqlar_soni DESC
    LIMIT 5
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# So‘rov 2: Eng ko‘p ishlatilgan tarif rejasi
def top_tarif():
    conn = get_connection()
    query = """
    SELECT tarif_rejasi, COUNT(*) AS soni
    FROM abonentlar
    GROUP BY tarif_rejasi
    ORDER BY soni DESC
    LIMIT 1
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# So‘rov 3: Hududlar bo‘yicha foydalanuvchilar soni
def users_by_region():
    conn = get_connection()
    query = """
    SELECT hudud, COUNT(*) AS abonentlar_soni
    FROM abonentlar
    GROUP BY hudud
    ORDER BY abonentlar_soni DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# So‘rov 4: Ism bo‘yicha qidirish
def search_by_name(name):
    conn = get_connection()
    query = """
    SELECT id, ism, familiya, raqam, tarif_rejasi, hudud
    FROM abonentlar
    WHERE ism LIKE ?
    """
    df = pd.read_sql_query(query, conn, params=('%' + name + '%',))
    conn.close()
    return df

# So‘rov 5: Oxirgi 30 kunda ulangan abonentlar
def new_users_last_30_days():
    conn = get_connection()
    query = """
    SELECT ism, familiya, faollashtirilgan
    FROM abonentlar
    WHERE faollashtirilgan >= ?
    ORDER BY faollashtirilgan DESC
    """
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    df = pd.read_sql_query(query, conn, params=(start_date,))
    conn.close()
    return df

# Streamlit UI
st.title("📡 Telekommunikatsiya Abonentlari Monitoring Ilovasi")

menu = st.sidebar.radio("So‘rov tanlang", [
    "Eng ko‘p qo‘ng‘iroq qilganlar",
    "Eng ko‘p ishlatilgan tarif",
    "Hududlar bo‘yicha abonentlar",
    "Ism bo‘yicha qidirish",
    "Oxirgi 30 kunda ulanganlar"
])

if menu == "Eng ko‘p qo‘ng‘iroq qilganlar":
    st.subheader("📞 Eng ko‘p qo‘ng‘iroq qilgan 5 abonent")
    st.dataframe(top_caller())

elif menu == "Eng ko‘p ishlatilgan tarif":
    st.subheader("💼 Eng ko‘p ishlatilgan tarif rejasi")
    st.dataframe(top_tarif())

elif menu == "Hududlar bo‘yicha abonentlar":
    st.subheader("📍 Hududlar bo‘yicha abonentlar soni")
    st.dataframe(users_by_region())

elif menu == "Ism bo‘yicha qidirish":
    st.subheader("🔍 Abonentni ism bo‘yicha qidirish")
    name = st.text_input("Ism kiriting:")
    if name:
        df = search_by_name(name)
        st.dataframe(df)

elif menu == "Oxirgi 30 kunda ulanganlar":
    st.subheader("🕒 Oxirgi 30 kunda ulangan abonentlar")
    st.dataframe(new_users_last_30_days())
