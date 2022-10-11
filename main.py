import logging

from aiogram import Bot, Dispatcher, executor, types

# Токен, выданный BotFather в телеграмме
API_TOKEN = ""

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def handler(message: types.Message):
    await message.answer(text="hello world")

dp.message_handler(handler)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)