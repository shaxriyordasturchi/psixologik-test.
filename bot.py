import sqlite3
from datetime import datetime, timedelta
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Ma'lumotlar bazasiga ulanish funksiyasi
def get_connection():
    return sqlite3.connect("telekom.db", check_same_thread=False)

# So'rovlar funksiyalari

def top_caller():
    conn = get_connection()
    query = """
    SELECT ism, familiya, COUNT(q.id) AS qongiroqlar_soni
    FROM abonentlar a
    JOIN chiquvchi_qongiroqlar q ON a.id = q.abonent_id
    GROUP BY a.id
    ORDER BY qongiroqlar_soni DESC
    LIMIT 5
    """
    cursor = conn.execute(query)
    natija = cursor.fetchall()
    conn.close()
    text = "📞 Eng ko'p qo'ng'iroq qilgan 5 abonent:\n"
    for ism, familiya, soni in natija:
        text += f"- {ism} {familiya}: {soni} qo'ng'iroq\n"
    return text

def top_tarif():
    conn = get_connection()
    query = """
    SELECT tarif_rejasi, COUNT(*) AS soni
    FROM abonentlar
    GROUP BY tarif_rejasi
    ORDER BY soni DESC
    LIMIT 1
    """
    cursor = conn.execute(query)
    natija = cursor.fetchone()
    conn.close()
    if natija:
        return f"💼 Eng ko'p ishlatilgan tarif rejasi: {natija[0]} ({natija[1]} abonent)"
    else:
        return "Ma'lumot topilmadi."

def users_by_region():
    conn = get_connection()
    query = """
    SELECT hudud, COUNT(*) AS abonentlar_soni
    FROM abonentlar
    GROUP BY hudud
    ORDER BY abonentlar_soni DESC
    """
    cursor = conn.execute(query)
    natija = cursor.fetchall()
    conn.close()
    text = "📍 Hududlar bo'yicha abonentlar soni:\n"
    for hudud, soni in natija:
        text += f"- {hudud}: {soni}\n"
    return text

def search_by_name(name):
    conn = get_connection()
    query = """
    SELECT ism, familiya, raqam, tarif_rejasi, hudud
    FROM abonentlar
    WHERE ism LIKE ?
    """
    cursor = conn.execute(query, ('%' + name + '%',))
    natija = cursor.fetchall()
    conn.close()
    if not natija:
        return f"🔍 '{name}' ismli abonent topilmadi."
    text = f"🔍 '{name}' ismli abonentlar:\n"
    for ism, familiya, raqam, tarif, hudud in natija:
        text += f"- {ism} {familiya}, {raqam}, Tarif: {tarif}, Hudud: {hudud}\n"
    return text

def new_users_last_30_days():
    conn = get_connection()
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    query = """
    SELECT ism, familiya, faollashtirilgan
    FROM abonentlar
    WHERE faollashtirilgan >= ?
    ORDER BY faollashtirilgan DESC
    """
    cursor = conn.execute(query, (start_date,))
    natija = cursor.fetchall()
    conn.close()
    if not natija:
        return "🕒 Oxirgi 30 kunda ulangan abonent topilmadi."
    text = "🕒 Oxirgi 30 kunda ulangan abonentlar:\n"
    for ism, familiya, sana in natija:
        text += f"- {ism} {familiya}, Faollashtirilgan: {sana}\n"
    return text

# Bot komandalariga javob berish

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Salom! Telekom botga xush kelibsiz.\n\n"
        "Quyidagi komandalarni ishlatishingiz mumkin:\n"
        "/top_caller - Eng ko'p qo'ng'iroq qilgan abonentlar\n"
        "/top_tarif - Eng ko'p ishlatilgan tarif\n"
        "/region_users - Hududlar bo'yicha abonentlar\n"
        "/search_name - Ism bo'yicha qidirish (misol: /search_name Ali)\n"
        "/new_users - Oxirgi 30 kunda ulanganlar"
    )

def top_caller_command(update: Update, context: CallbackContext) -> None:
    text = top_caller()
    update.message.reply_text(text)

def top_tarif_command(update: Update, context: CallbackContext) -> None:
    text = top_tarif()
    update.message.reply_text(text)

def region_users_command(update: Update, context: CallbackContext) -> None:
    text = users_by_region()
    update.message.reply_text(text)

def search_name_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Iltimos, ismni kiriting. Misol: /search_name Ali")
        return
    name = ' '.join(context.args)
    text = search_by_name(name)
    update.message.reply_text(text)

def new_users_command(update: Update, context: CallbackContext) -> None:
    text = new_users_last_30_days()
    update.message.reply_text(text)

def main():
    TOKEN = "7917375202:AAGhRKgMa9H9SYhyZR6mWXM1sjg5RBhTUx0"  # TOKENni shu yerga qo'ying
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("top_caller", top_caller_command))
    dispatcher.add_handler(CommandHandler("top_tarif", top_tarif_command))
    dispatcher.add_handler(CommandHandler("region_users", region_users_command))
    dispatcher.add_handler(CommandHandler("search_name", search_name_command))
    dispatcher.add_handler(CommandHandler("new_users", new_users_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
