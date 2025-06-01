from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sqlite3
import pandas as pd

TOKEN = "7917375202:AAGhRKgMa9H9SYhyZR6mWXM1sjg5RBhTUx0"

def get_connection():
    return sqlite3.connect("telekom.db")

def start(update: Update, context: CallbackContext):
    keyboard = [['Eng ko‘p qo‘ng‘iroq qilganlar', 'Eng ko‘p ishlatilgan tarif'],
                ['Hududlar bo‘yicha abonentlar', 'Ism bo‘yicha qidirish'],
                ['Oxirgi 30 kunda ulanganlar']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Telekom monitoring botiga xush kelibsiz! So‘rovni tanlang:', reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    conn = get_connection()

    if text == 'Eng ko‘p qo‘ng‘iroq qilganlar':
        query = """
        SELECT ism, familiya, COUNT(q.id) AS qongiroqlar_soni
        FROM abonentlar a
        JOIN chiquvchi_qongiroqlar q ON a.id = q.abonent_id
        GROUP BY a.id
        ORDER BY qongiroqlar_soni DESC
        LIMIT 5
        """
        df = pd.read_sql_query(query, conn)
        msg = "\n".join([f"{row['ism']} {row['familiya']}: {row['qongiroqlar_soni']} qo‘ng‘iroq" for idx, row in df.iterrows()])
        update.message.reply_text(msg)

    elif text == 'Eng ko‘p ishlatilgan tarif':
        query = """
        SELECT tarif_rejasi, COUNT(*) AS soni
        FROM abonentlar
        GROUP BY tarif_rejasi
        ORDER BY soni DESC
        LIMIT 1
        """
        df = pd.read_sql_query(query, conn)
        if not df.empty:
            row = df.iloc[0]
            update.message.reply_text(f"Eng ko‘p ishlatilgan tarif: {row['tarif_rejasi']} ({row['soni']} abonent)")
        else:
            update.message.reply_text("Ma'lumot topilmadi.")

    elif text == 'Hududlar bo‘yicha abonentlar':
        query = """
        SELECT hudud, COUNT(*) AS abonentlar_soni
        FROM abonentlar
        GROUP BY hudud
        ORDER BY abonentlar_soni DESC
        """
        df = pd.read_sql_query(query, conn)
        msg = "\n".join([f"{row['hudud']}: {row['abonentlar_soni']} abonent" for idx, row in df.iterrows()])
        update.message.reply_text(msg)

    elif text == 'Ism bo‘yicha qidirish':
        update.message.reply_text("Iltimos, qidiriladigan ismingizni yuboring:")
        context.user_data['search_name'] = True

    elif text == 'Oxirgi 30 kunda ulanganlar':
        query = """
        SELECT ism, familiya, faollashtirilgan
        FROM abonentlar
        WHERE faollashtirilgan >= date('now', '-30 day')
        ORDER BY faollashtirilgan DESC
        """
        df = pd.read_sql_query(query, conn)
        msg = "\n".join([f"{row['ism']} {row['familiya']} — {row['faollashtirilgan']}" for idx, row in df.iterrows()])
        update.message.reply_text(msg)

    else:
        # Agar foydalanuvchi ism bo‘yicha qidirishni boshlagan bo‘lsa
        if context.user_data.get('search_name'):
            name = text
            query = """
            SELECT ism, familiya, raqam, tarif_rejasi, hudud
            FROM abonentlar
            WHERE ism LIKE ?
            """
            df = pd.read_sql_query(query, conn, params=(f"%{name}%",))
            if not df.empty:
                msg = "\n".join([f"{row['ism']} {row['familiya']} — {row['raqam']} — {row['tarif_rejasi']} — {row['hudud']}" for idx, row in df.iterrows()])
                update.message.reply_text(msg)
            else:
                update.message.reply_text("Hech qanday abonent topilmadi.")
            context.user_data['search_name'] = False
        else:
            update.message.reply_text("Noto‘g‘ri buyruq. Iltimos, menyudan tanlang.")

    conn.close()

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
