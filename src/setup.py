from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

# create routes

user_router = Router()
# common_router = Router()

BASE_DIR = os.path.dirname(__file__)

admins = {713711218,
          1137700340,
          5459347964,
          286365412
          }


files = {
    'california': [
        'california',
        'Adriana Insurance',
        'All State Insurance Company',
        'Bristol West Insurance Company',
        'Direct Auto Insurance Company',
        'Farmers Insurance Company'],
    'illinois': ['Falcon', 'UniqueID'],
    'pennsylvania': []
}
