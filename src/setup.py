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

admins = {286365412,
          713711218,
          1137700340,
          5459347964,
          286365412,
          475396264,
          5645161603,
          5501113966,
          5340595935,
          829278587}

# admins = {713711218,
#           1137700340,
#           5459347964,
#           286365412
#           }


files = {
    'California': [
        'Mercury Insurance CA',
        'Adriana Insurance CA',
        'All State Insurance CA'
    ],
    'Illinois': [
        'Falcon IL', 'UniqueID',
        "Direct Auto Insurance IL",
        "Bristol West Insurance IL",
        "Clearcover Insurance IL"
    ],
    'Pennsylvania': [
        'Bristol West Insurance PA',
        'Direct Auto Insurance PA',
        'Farmers Insurance PA'
    ],
    'Florida': [
        "Safeco Insurance FL",
        "Direct Auto Insurance FL",
        "Pronto Insurance FL"

    ],
    'Washington': [
        "Insurance Services of Washington WA",
        "Travelers Insurance WA",
        "Country Financial Insurance WA"
    ],
    'Massachusetts': [
        "Lighthouse Insurance MA",
        "Eagle Trust Insurance MA",
        "Gvy Insurance Insurance MA"
    ]
}

cities = files.keys()
