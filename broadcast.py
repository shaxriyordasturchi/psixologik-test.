from db import get_all_abonents

async def broadcast_message(bot, text):
    abonents = get_all_abonents()
    count = 0
    for _, name, chat_id in abonents:
        try:
            await bot.send_message(chat_id=chat_id, text=f"📢 E'lon: {text}")
            count += 1
        except Exception as e:
            print(f"Xatolik yuborishda {chat_id}: {e}")
    return count
