from aiogram import Dispatcher, Bot
from utils import config

bot = Bot(config.get_config()["token"])
dp = Dispatcher(bot)