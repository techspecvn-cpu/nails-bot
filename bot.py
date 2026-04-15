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


@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text.lower()

    state = user_state.get(user_id)

    if text == "1":
        user_state[user_id] = "waiting_date"
        await message.answer("Отлично 💅 Напиши удобную дату")

    elif state == "waiting_date":
        user_state[user_id] = {"step": "waiting_time", "date": message.text}
        await message.answer("Теперь напиши удобное время ⏰")

    elif isinstance(state, dict) and state.get("step") == "waiting_time":
        date = state["date"]
        time = message.text
        user_state[user_id] = None

        await message.answer(
            f"Записала тебя 💖\nДата: {date}\nВремя: {time}\n\nЖдём тебя 🌸"
        )

    elif text == "2":
        user_state[user_id] = "chat"
        await message.answer("Я рядом 💖 Расскажи, что тебя беспокоит")

    elif state == "chat":
        if "груст" in text:
            await message.answer("Мне жаль, что тебе так 😔 Хочешь поговорить об этом?")
        elif "скуч" in text:
            await message.answer("Скука — это сигнал ✨ Может, пора порадовать себя маникюром? 💅")
        else:
            await message.answer("Я слушаю тебя 🤍 Расскажи подробнее")

    else:
        await message.answer("Напиши 1 — запись или 2 — поговорить 😊")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
