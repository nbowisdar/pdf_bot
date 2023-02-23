from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,\
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.setup import cities

kb1 = [
    [KeyboardButton(text="❌ Cancel")]
]
kb2 = [
    [KeyboardButton(text="Заказать")],
    [KeyboardButton(text="Отмена")]
]

kb3 = [
    [KeyboardButton(text="California"),
     KeyboardButton(text="Chicago"),
     KeyboardButton(text="Отмена")],
]

cancel_btn = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)
order_btn = ReplyKeyboardMarkup(
    keyboard=kb2,
    resize_keyboard=True
)
choose_city_btn = ReplyKeyboardMarkup(
    keyboard=kb3,
    resize_keyboard=True
)

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🌪 Insurance'), KeyboardButton(text='✍️ Registration')]
    ],
    resize_keyboard=True
)


def build_cities_btns():
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.add(
            InlineKeyboardButton(text=f"{city}",
                                 callback_data=f"city|{city}")
        )
    builder.adjust(2)
    return builder.as_markup()

# in_kb1 = [
#
#     [InlineKeyboardButton(text="🏰 Illinois",
#                           callback_data="city|illinois"),
#      InlineKeyboardButton(text="🏙 California",
#                           callback_data="city|california")],
#     [InlineKeyboardButton(text="🌆 Pennsylvania",
#                           callback_data="city|pennsylvania")]
# ]

# city_kb = InlineKeyboardMarkup(
#     inline_keyboard=in_kb1
# )


async def choose_version(variants: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for var in variants:
        builder.add(InlineKeyboardButton(
            text=var, callback_data=f"var|{var}"
        ))
    builder.adjust(1)
    return builder.as_markup()