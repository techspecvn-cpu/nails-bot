import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = "8452593173:AAHSfC20tszMT3la1-9p0AZoLY0DCcGwO3E"

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_state = {}

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 💅\n"
        "Я бот записи на маникюр и поддержки 💖\n\n"
        "Напиши:\n"
        "1 — Записаться\n"
        "2 — Поговорить"
    )


user_data = {}
ADMIN_ID = 1505361956  # ← ЗАМЕНИ на свой Telegram ID

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in user_data:
        user_data[user_id] = {"state": None}

    state = user_data[user_id].get("state")

    # СТАРТ
    if text == "/start":
        user_data[user_id] = {"state": None}
        await message.answer(
            "Привет! 💅\nЯ бот записи\n\n1 — Записаться\n2 — Поговорить"
        )

    elif text == "1" and state is None:
        user_data[user_id]["state"] = "name"
        await message.answer("Как тебя зовут?")

    elif state == "name":
        user_data[user_id]["name"] = text
        user_data[user_id]["state"] = "service"

        await message.answer(
            "Выбери услугу:\nМаникюр / Педикюр / Наращивание"
        )

    elif state == "service":
        user_data[user_id]["service"] = text
        user_data[user_id]["state"] = "date"
        await message.answer("Напиши дату (например: 25 марта)")

    elif state == "date":
        user_data[user_id]["date"] = text
        user_data[user_id]["state"] = "time"
        await message.answer("Напиши время")

    elif state == "time":
        user_data[user_id]["time"] = text
        user_data[user_id]["state"] = None

        data = user_data[user_id]

        # сообщение клиенту
        await message.answer(
            f"💖 Ты записана!\n\n"
            f"Имя: {data['name']}\n"
            f"Услуга: {data['service']}\n"
            f"Дата: {data['date']}\n"
            f"Время: {data['time']}\n\n"
            f"Если нужно отменить — напиши: отмена"
        )

        # сообщение мастеру
        await bot.send_message(
            ADMIN_ID,
            f"🔥 Новая запись!\n\n"
            f"Имя: {data['name']}\n"
            f"Услуга: {data['service']}\n"
            f"Дата: {data['date']}\n"
            f"Время: {data['time']}"
        )

    elif text.lower() == "отмена":
        await message.answer("❌ Запись отменена")
        await bot.send_message(ADMIN_ID, "❌ Клиент отменил запись")

    elif text == "2":
        user_data[user_id]["state"] = "chat"
        await message.answer("Я рядом 💖 Расскажи, что тебя беспокоит")

    elif state == "chat":
        if "нет времени" in text.lower():
            await message.answer(
                "Понимаю 💔 Давай подберём другое время 🙏"
            )
        else:
            await message.answer("Я тебя слышу 💖 Расскажи подробнее")

    else:
        await message.answer("Напиши 1 — запись или 2 — поговорить 😊")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
