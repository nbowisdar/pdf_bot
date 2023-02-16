from loguru import logger
from aiogram import F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from docxtpl import DocxTemplate

from setup import user_router
from utils.convert_files import convert_docx_to_pdf

kb1 = [
    [KeyboardButton(text="Отмена")]
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


class OrdrState(StatesGroup):
    name = State()
    make_model = State()
    vin_number = State()
    city = State()


class FullState(StatesGroup):
    data = State()


@user_router.message(Text(text='Отмена'))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Отменено",
        reply_markup=order_btn)


@user_router.message(Text(text="Заказать"))
async def set_full_data(message: Message, state: FSMContext):
    await state.set_state(FullState.data)
    await message.answer("*First Middle Lastname\n"
                         "Year Make Model\n"
                         "Viin Number\n"
                         "City*\n\n"
                         "_In one message, For example:_\n\n"
                         "`OMAR IBN ALHATTAB\n"
                         "2002 TOYOTA PRIUS\n"
                         "JT2BK12UX20056855\n"
                         "Chicago or California`", parse_mode="MARKDOWN")


@user_router.message(FullState.data)
async def set_full_data(message: Message, state: FSMContext):
    #try:
    messages = message.text.split("\n")
    data = {'name': messages[0], 'model': messages[1], 'vin': messages[2], 'city': messages[3]}
    await send_file(data, message)
    #except Exception as e:
    #    logger.error(e)
    #    await message.reply('Error, try again')
    await state.clear()


async def send_file(data, message):
    #convertapi.api_secret = 'W2bfIxig2LpvEp8e'
    doc = None
    context = {}
    if data['city'] == 'California':
        doc = DocxTemplate("templates/california.docx")
        context = {'NAME': data['name'], 'car': data['model'], 'VIIN': data['vin']}
    elif data['city'] == 'Chicago':
        doc = DocxTemplate("templates/illinois.docx")
        context = {'name': data['name'], 'car': data['model'], 'viin': data['vin']}
    doc.render(context)
    file_name = 'final.docx'
    doc.save(file_name)
    await message.reply('Ожидайте PDF файл...')
    file = convert_docx_to_pdf(file_name)
    document = BufferedInputFile(file, filename='res.pdf')
    #     send this file with reply
    await message.reply_document(document=document, caption=f"{data['name']} - {data.get('city')}")
