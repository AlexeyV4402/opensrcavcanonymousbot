from aiogram import Dispatcher, Bot, F
from aiogram.fsm.storage.memory import MemoryStorage

import config

storage = MemoryStorage()

bot = Bot(config.TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
