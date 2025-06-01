import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler,
    MessageHandler, filters, CallbackQueryHandler
)
import db
import network_status
import broadcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ADD_NAME = 1
REMOVE_ID = 2

ADMIN_ID = 123456789  # O'zingizning Telegram IDingizni yozing

# --- Bot komandalar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Abonent qo‘shish", callback_data='add')],
        [InlineKeyboardButton("📋 Abonentlar ro‘yxati", callback_data='list')],
        [InlineKeyboardButton("❌ Abonent o‘chirish", callback_data='remove')],
        [InlineKeyboardButton("📡 Tarmoq holati", callback_data='status')],
        [InlineKeyboardButton("⚠️ Ogohlantirishlar", callback_data='alerts')],
        [InlineKeyboardButton("📢 Xabar tarqatish", callback_data='broadcast')],
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

    if data == 'add':
        await query.message.reply_text("Iltimos, abonent ismini kiriting:")
        return ADD_NAME
    elif data == 'list':
        abonents = db.get_all_abonents()
        if not abonents:
            await query.message.reply_text("Hozircha abonentlar mavjud emas.")
        else:
            msg = "Abonentlar ro‘yxati:\n"
            for abonent_id, name, _ in abonents:
                msg += f"{abonent_id}: {name}\n"
            await query.message.reply_text(msg)
        await start(update, context)
        return ConversationHandler.END
    elif data == 'remove':
        await query.message.reply_text("O‘chirish uchun abonent ID ni kiriting:")
        return REMOVE_ID
    elif data == 'status':
        status = network_status.get_network_status()
        await query.message.reply_text(status)
        await start(update, context)
        return ConversationHandler.END
    elif data == 'alerts':
        alerts = network_status.get_alerts()
        msg = "So‘nggi ogohlantirishlar:\n" + "\n".join(alerts)
        await query.message.reply_text(msg)
        await start(update, context)
        return ConversationHandler.END
    elif data == 'broadcast':
        if query.from_user.id != ADMIN_ID:
            await query.message.reply_text("Sizda bu komanda uchun ruxsat yo‘q.")
            return ConversationHandler.END
        await query.message.reply_text("Iltimos, tarqatmoqchi bo‘lgan xabaringizni kiriting:")
        return REMOVE_ID + 1  # broadcast uchun yangi state
    else:
        await query.message.reply_text("Noto‘g‘ri amal tanlandi.")
        return ConversationHandler.END

async def add_abonent_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    chat_id = update.message.from_user.id
    if not name:
        await update.message.reply_text("Ism bo‘sh bo‘lishi mumkin emas. Qaytadan kiriting:")
        return ADD_NAME
    added = db.add_abonent(name, chat_id)
    if not added:
        await update.message.reply_text("Abonent allaqachon ro‘yxatda mavjud.")
    else:
        await update.message.reply_text(f"Abonent '{name}' muvaffaqiyatli qo‘shildi.")
    await start(update, context)
    return ConversationHandler.END

async def remove_abonent_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input.isdigit():
        await update.message.reply_text("Iltimos, faqat raqam kiriting.")
        return REMOVE_ID
    abonent_id = int(user_input)
    deleted = db.remove_abonent(abonent_id)
    if deleted:
        await update.message.reply_text(f"Abonent ID {abonent_id} muvaffaqiyatli o‘chirildi.")
    else:
        await update.message.reply_text(f"ID {abonent_id} ga ega abonent topilmadi.")
    await start(update, context)
    return ConversationHandler.END

async def broadcast_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != 7750409176:
        await update.message.reply_text("Sizda bu komanda uchun ruxsat yo‘q.")
        return ConversationHandler.END
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("Xabar bo‘sh bo‘lishi mumkin emas. Qaytadan kiriting:")
        return REMOVE_ID + 1
    count = await broadcast.broadcast_message(context.bot, text)
    await update.message.reply_text(f"{count} abonentga xabar yuborildi.")
    await start(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Amal bekor qilindi.")
    await start(update, context)
    return ConversationHandler.END

def main():
    db.init_db()

    BOT_TOKEN = "7917375202:AAGhRKgMa9H9SYhyZR6mWXM1sjg5RBhTUx0"

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            ADD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_abonent_name)],
            REMOVE_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, remove_abonent_id)
            ],
            REMOVE_ID + 1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message_handler)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
