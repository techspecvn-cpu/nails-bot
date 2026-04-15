import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = "8452593173:AAHSfC20tszMT3la1-9p0AZoLY0DCcGwO3E"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
ADMIN_ID = 1505361956  # замени если нужно

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записаться")],
        [KeyboardButton(text="Поговорить")]
    ],
    resize_keyboard=True
)

service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Маникюр")],
        [KeyboardButton(text="Педикюр")],
        [KeyboardButton(text="Наращивание")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 💅\nЯ бот записи на маникюр 💖",
        reply_markup=main_kb
    )

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text or ""   # ✅ защита от None

    if user_id not in user_data:
        user_data[user_id] = {"state": None}

    state = user_data[user_id].get("state")

    if text == "/start":
        user_data[user_id] = {"state": None}
        await message.answer("Привет 💅", reply_markup=main_kb)

    elif text == "Записаться":
        user_data[user_id]["state"] = "name"
        await message.answer("Как тебя зовут?")

    elif state == "name":
        user_data[user_id]["name"] = text
        user_data[user_id]["state"] = "service"
        await message.answer("Выбери услугу:", reply_markup=service_kb)

    elif state == "service":
        if text == "Отмена":
            user_data[user_id]["state"] = None
            await message.answer("Отменено", reply_markup=main_kb)
            return

        user_data[user_id]["service"] = text
        user_data[user_id]["state"] = "date"
        await message.answer("Напиши дату (например: 25 марта)")

    elif state == "date":
        if text in ["Записаться", "Поговорить", "Маникюр", "Педикюр", "Наращивание"]:
        await message.answer("Сейчас нужно ввести дату 🙏 Например: 25 марта")
        return

        if len(text) < 3:
        await message.answer("Напиши нормальную дату 🙏 Например: 25 марта")
        return

    user_data[user_id]["date"] = text
    user_data[user_id]["state"] = "time"
    await message.answer("Напиши время")    

    elif state == "time":
       if text in ["Записаться", "Поговорить", "Маникюр", "Педикюр", "Наращивание"]:
        await message.answer("Сейчас нужно ввести время 🙏 Например: 14:00")
        return

    user_data[user_id]["time"] = text
    user_data[user_id]["state"] = None

    data = user_data[user_id]

    await message.answer(
        f"💖 Ты записана!\n\n"
        f"Имя: {data['name']}\n"
        f"Услуга: {data['service']}\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}\n\n"
        f"Если нужно отменить — напиши: отмена",
        reply_markup=main_kb
    )

    await bot.send_message(
        ADMIN_ID,
        f"🔥 Новая запись!\n\n"
        f"Имя: {data['name']}\n"
        f"Услуга: {data['service']}\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}"
    )
    
    elif text.lower() == "отмена":
        await message.answer("❌ Запись отменена", reply_markup=main_kb)
        await bot.send_message(ADMIN_ID, "❌ Клиент отменил запись")

    elif text == "Поговорить":
        user_data[user_id]["state"] = "chat"
        await message.answer("Я рядом 💖 Расскажи, что тебя беспокоит")

    elif state == "chat":
        if "нет времени" in text.lower():
            await message.answer("Понимаю 💔 Давай подберём другое время 🙏")
        else:
            await message.answer("Я тебя слышу 💖 Расскажи подробнее")

    else:
        await message.answer("Выбери кнопку ниже 👇", reply_markup=main_kb)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
