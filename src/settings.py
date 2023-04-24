import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

TOKEN = os.getenv('TOKEN')

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@127.0.0.1:5434/{DB_NAME}'

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', default=30))
SECRET_KEY: str = os.getenv('SECRET_KEY', default='secret_key')
ALGORITHM: str = os.getenv('ALGORITHM', default='HS256')
