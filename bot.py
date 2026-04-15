def normalize_time(text):
    text = text.lower().replace("в ", "").replace("часов", "").replace("час", "").strip()

    if ":" in text:
        return text

    if text.isdigit():
        return f"{text}:00"

    return text

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = "8452593173:AAHSfC20tszMT3la1-9p0AZoLY0DCcGwO3E"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
ADMIN_ID = 1505361956  # замени если нужно

# КЛАВИАТУРЫ
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

# СТАРТ
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 💅\nЯ бот записи на маникюр 💖",
        reply_markup=main_kb
    )

# ОСНОВНАЯ ЛОГИКА
@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in user_data:
        user_data[user_id] = {"state": None}

    state = user_data[user_id].get("state")

    # НАЧАЛО ЗАПИСИ
    if text == "Записаться" and state is None:
        user_data[user_id]["state"] = "name"
        await message.answer("Как тебя зовут?")

    elif state == "name":
        user_data[user_id]["name"] = text
        user_data[user_id]["state"] = "service"
        await message.answer("Выбери услугу:", reply_markup=service_kb)

    elif state == "service":
        if text == "Отмена":
            user_data[user_id]["state"] = None
            await message.answer("Запись отменена ❌", reply_markup=main_kb)
            return

        user_data[user_id]["service"] = text
        user_data[user_id]["state"] = "date"
        await message.answer("Напиши дату (например: 25 марта)")

    elif state == "date":
        if text in ["Записаться", "Поговорить", "Маникюр", "Педикюр", "Наращивание"]:
            await message.answer("Сначала введи дату 🙏 Например: 25 марта")
            return

        user_data[user_id]["date"] = text
        user_data[user_id]["state"] = "time"
        await message.answer("Напиши время (например: 14:00)")

    elif state == "time":
        if text in ["Записаться", "Поговорить", "Маникюр", "Педикюр", "Наращивание"]:
            await message.answer("Сначала введи время 🙏 Например: 14:00")
            return

        time = normalize_time(text)
        user_data[user_id]["time"] = time
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

    return
 
        elif state == "time":
            if text in ["Записаться", "Поговорить", "Маникюр", "Педикюр", "Наращивание"]:
                await message.answer("Сначала введи время 🙏 Например: 14:00")
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

        return

    if text.lower() == "отмена":
        user_data[user_id]["state"] = None
        await message.answer("❌ Запись отменена", reply_markup=main_kb)
        await bot.send_message(ADMIN_ID, "❌ Клиент отменил запись")

    elif text == "Поговорить":
        user_data[user_id]["state"] = "chat"
        await message.answer("Я рядом 💖 Расскажи, что тебя беспокоит")

    elif state == "chat":
        text_lower = text.lower()

        if any(word in text_lower for word in ["нет времени", "занято", "не могу", "окна", "свободно"]):
            await message.answer("Понимаю 💔 Давай подберём удобное время 🙏 Когда тебе удобно?")
    
        elif any(word in text_lower for word in ["мастер", "свободен", "занят"]):
            await message.answer("Я уточню по мастеру 💅 Напиши дату, которая тебе подходит")

        elif any(word in text_lower for word in ["цена", "сколько", "стоимость", "дорого"]):
            await message.answer("Цена зависит от услуги 💅 Напиши, что именно хочешь — подскажу 💖")

        elif any(word in text_lower for word in ["давай", "ок", "хорошо"]):
            user_data[user_id]["state"] = "service"
            await message.answer("Отлично 💖 Выбери услугу:", reply_markup=service_kb)

        else:
            await message.answer("Я рядом 💖 Давай подберём удобную запись")

# ЗАПУСК
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
