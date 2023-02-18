from src.setup import files
from loguru import logger
from aiogram import F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from docxtpl import DocxTemplate

from src.keyboards import order_btn, start_kb, city_kb, cancel_btn, choose_version
from src.setup import user_router
from utils.convert_files import convert_docx_to_pdf


# class OrdrState(StatesGroup):
#     name = State()
#     make_model = State()
#     vin_number = State()
#     city = State()

class RegistrationState(StatesGroup):
    data = State()


class FullState(StatesGroup):
    city = State()
    variant = State()
    data = State()


@user_router.message(F.text == "/start")
async def start(message: Message):
    await message.answer('Options', reply_markup=start_kb)


@user_router.message(Text(text='❌ Cancel'))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Отменено",
        reply_markup=start_kb)


@user_router.message(Text(text="✍️ Registration"))
async def set_full_data(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.data)
    await message.answer("*First Middle Lastname\n"
                         "Address\n"
                         "Viin Number\n"
                         "Vehicle Year\n"
                         "Vehicle Make\n"
                         "Body Style\n"
                         "Plate Number*\n"
                         "_In one message, For example:_\n\n"
                         "`OMAR ADIL JOMART\n"
                         "2750 W SUMMERDALE AVE APT 2, CHICAGO, IL 6065\n"
                         "4T1BB46K18U045113\n"
                         "2008\n"
                         "TOYOTA\n"
                         "SEDAN\n"
                         "DN81889`", parse_mode="MARKDOWN", reply_markup=cancel_btn)


@user_router.message(RegistrationState.data)
async def set_full_data(message: Message, state: FSMContext):
    try:
        messages = message.text.split("\n")
        data = {
            'NAME': messages[0],
            'ADDRESS': messages[1],
            'VIN': messages[2],
            'YEAR': messages[3],
            'MAKE': messages[4],
            'STYLE': messages[5],
            'PLATE': messages[6],
            'NUMBER': messages[2][-3:]
        }
        await send_file_il(data, message)
    except Exception as e:
        logger.error(e)
        await message.reply('Error')
    await state.clear()


async def send_file_il(data, message):
    doc = DocxTemplate("templates/registration.docx")
    context = {
        'NAME': data.get('NAME'),
        'ADDRESS': data.get('ADDRESS'),
        'VIN': data.get('VIN'),
        'YEAR': data.get('YEAR'),
        'MAKE': data.get('MAKE'),
        'STYLE': data.get('STYLE'),
        'PLATE': data.get('PLATE'),
        'NUMBER': data.get('NUMBER'),
    }
    doc.render(context)
    file_name = 'final.docx'
    doc.save(file_name)
    await message.reply('Ожидайте PDF файл...')
    file = convert_docx_to_pdf(file_name)
    document = BufferedInputFile(file, filename='res.pdf')
    await message.reply_document(document=document, caption=f"Generated - {data['NAME']}",
                                 reply_markup=start_kb)



@user_router.message(F.text == "🌪 Insurance")
async def start(message: Message, state: FSMContext):
    # await state.set_state(FullState.city)
    await message.answer('Choose city:', reply_markup=city_kb)
# choose_version


@user_router.callback_query(Text(startswith="city"))
async def set_full_data(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split('|')[1]
    variants = files.get(city)
    await state.update_data(city=city)
    await state.set_state(FullState.variant)
    await callback.message.edit_text("Select variant ✂️",
                                     reply_markup=await choose_version(variants))

    await callback.answer()


@user_router.callback_query(Text(startswith="var"))
async def set_full_data(callback: CallbackQuery, state: FSMContext):
    variant = callback.data.split('|')[1]
    await state.update_data(variant=variant)
    await state.set_state(FullState.data)
    await callback.message.answer("*First Middle Lastname\n"
                                  "Year Make Model\n"
                                  "Viin Number*\n\n"
                                  "_In one message, For example:_\n\n"
                                  "`OMAR IBN ALHATTAB\n"
                                  "2002 TOYOTA PRIUS\n"
                                  "JT2BK12UX20056855`\n", parse_mode="MARKDOWN",
                                  reply_markup=cancel_btn)
    await callback.answer()


@user_router.message(FullState.data)
async def set_full_data(message: Message, state: FSMContext):
    try:
        messages = message.text.split("\n")
        data = {'name': messages[0], 'model': messages[1], 'vin': messages[2]}
        data.update(await state.get_data())
        await send_file(data, message)
    except Exception as e:
        logger.error(e)
        await message.reply('Error')
    await state.clear()


async def send_file(data, message):
    doc = DocxTemplate(f"templates/{data['variant']}.docx")
    context = {'name': data['name'], 'car': data['model'], 'viin': data['vin']}
    doc.render(context)
    file_name = 'final.docx'
    doc.save(file_name)
    await message.reply('Ожидайте PDF файл...')
    file = convert_docx_to_pdf(file_name)
    document = BufferedInputFile(file, filename='res.pdf')
    await message.reply_document(document=document, caption=f"{data['name']} - {data.get('city')}",
                                 reply_markup=start_kb)
    logger.info(f"File sent - {data['name']}")
