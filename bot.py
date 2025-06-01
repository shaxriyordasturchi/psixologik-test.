import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler,
    MessageHandler, filters, CallbackQueryHandler
)

DB_NAME = "abonents.db"

ADD_NAME = 1
REMOVE_ID = 2

# --- DB funksiyalar ---
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

def add_abonent_to_db(name: str, chat_id: int):
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

def remove_abonent_by_id(abonent_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM abonents WHERE id = ?", (abonent_id,))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes

# --- Bot komandalar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Add Abonent", callback_data='addabonent')],
        [InlineKeyboardButton("📋 List Abonents", callback_data='listabonent')],
        [InlineKeyboardButton("❌ Remove Abonent", callback_data='removeabonent')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Quyidagi amallardan birini tanlang:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text("Quyidagi amallardan birini tanlang:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == 'addabonent':
        await query.message.reply_text("Iltimos, yangi abonent ismini kiriting:")
        return ADD_NAME
    elif data == 'listabonent':
        abonents = get_all_abonents()
        if not abonents:
            await query.message.reply_text("Hozircha abonentlar mavjud emas.")
        else:
            msg = "Abonentlar ro'yxati:\n"
            for abonent_id, name, _ in abonents:
                msg += f"{abonent_id}: {name}\n"
            await query.message.reply_text(msg)
        await start(update, context)
        return ConversationHandler.END
    elif data == 'removeabonent':
        await query.message.reply_text("O'chirish uchun abonent ID ni kiriting:")
        return REMOVE_ID
    elif data == 'cancel':
        await query.message.reply_text("Amal bekor qilindi.")
        await start(update, context)
        return ConversationHandler.END

async def addabonent_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    chat_id = update.message.from_user.id
    if not name:
        await update.message.reply_text("Ism bo'sh bo'lishi mumkin emas. Qaytadan kiriting:")
        return ADD_NAME
    added = add_abonent_to_db(name, chat_id)
    if not added:
        await update.message.reply_text(f"Abonent allaqachon ro'yxatda mavjud.")
    else:
        await update.message.reply_text(f"Abonent '{name}' muvaffaqiyatli qo'shildi.")
    await start(update, context)
    return ConversationHandler.END

async def removeabonent_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input.isdigit():
        await update.message.reply_text("Iltimos, faqat raqam kiriting.")
        return REMOVE_ID
    abonent_id = int(user_input)
    deleted = remove_abonent_by_id(abonent_id)
    if deleted:
        await update.message.reply_text(f"Abonent ID {abonent_id} muvaffaqiyatli o'chirildi.")
    else:
        await update.message.reply_text(f"ID {abonent_id} ga ega abonent topilmadi.")
    await start(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Amal bekor qilindi.")
    await start(update, context)
    return ConversationHandler.END

# --- Qo'shimcha komandalar ---

# /status komandasi
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    network_status = "Tarmoq holati: HAMMASI YAXSHI ✅\nHech qanday uzilish yoki xatoliklar yo‘q."
    await update.message.reply_text(network_status)

# /ogohlantirishlar komandasi
async def ogohlantirishlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts = [
        "12:15 da Router 5 da uzilish yuz berdi.",
        "13:40 da Switch 2 da paket yo'qotish kuzatildi.",
        "14:05 da Server 3 bilan aloqada muammo."
    ]
    msg = "So‘nggi ogohlantirishlar:\n" + "\n".join(alerts)
    await update.message.reply_text(msg)

# /broadcast komandasi
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ADMIN_ID = 123456789  # O'zingizning Telegram ID-ingizni yozing
    if update.message.from_user.id !=7750409176:
        await update.message.reply_text("Sizda bu komanda uchun ruxsat yo'q.")
        return
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Iltimos, xabar matnini kiriting. Misol: /broadcast Xizmatda uzilish bor.")
        return
    abonents = get_all_abonents()
    count = 0
    for _, name, chat_id in abonents:
        try:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Ogohlantirish: {text}")
            count += 1
        except Exception as e:
            print(f"Xatolik yuborishda: {e}")
    await update.message.reply_text(f"{count} abonentga xabar yuborildi.")

def main():
    init_db()
    BOT_TOKEN = "7917375202:AAGhRKgMa9H9SYhyZR6mWXM1sjg5RBhTUx0"

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^(addabonent|removeabonent|listabonent|cancel)$')],
        states={
            ADD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, addabonent_name)],
            REMOVE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, removeabonent_id)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)

    # Qo'shimcha komandalar
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('ogohlantirishlar', ogohlantirishlar))
    application.add_handler(CommandHandler('broadcast', broadcast))

    application.run_polling()

if __name__ == '__main__':
    main()
