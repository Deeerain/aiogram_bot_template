from aiogram.types import *
from bot.dispathcer import dp

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.bot.send_message(message.from_user.id, f"Hello, {message.from_user.full_name}!!!\nThis is basic template telegram bot!")