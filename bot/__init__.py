from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

# from bot.tokens import API_TOKEN

dotenv_path = '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
# from config import TOKEN

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Initialize bot, local storage and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
