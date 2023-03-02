from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dis = Dispatcher(bot, storage=MemoryStorage())
