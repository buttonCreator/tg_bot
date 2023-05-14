from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram_datepicker import DatepickerSettings
from create_bot import dp, storage
from keyboards import static_kb

from data_base import sqile_db
from keyboards.user_kb import marcup


class Form(StatesGroup):
    secondName = State()
    firstName = State()
    middleName = State()
    answer = State()


def _get_datepicker_settings():
    return DatepickerSettings()


async def string_validation(text, fieldForm, pattern, message: types.Message, state: FSMContext, markup=None):
    lower_text = text.lower()
    if lower_text.isalpha():
        async with state.proxy() as data:
            data[fieldForm] = message.text.lower()
        await Form.next()
        await message.answer(pattern, reply_markup=markup)
    else:
        await message.answer("Ну пж, введи норм")


def fio(data):
    secondName = data['secondName']
    firstName = data['firstName']
    thirdName = data['middleName']
    stroka = f'Давайте проверим Ваши данные.\nВас зовут: {secondName} {firstName} {thirdName} \n'
    return stroka


async def start_bot(message: types.Message):
    await Form.secondName.set()
    await message.answer('Чтобы я мог коректно работать, пожалуйста, авторизируйтесь\n\nВведите фамилию:', reply_markup=ReplyKeyboardRemove())


async def processSecondName(message: types.Message, state: FSMContext):
    await string_validation(message.text, 'secondName', 'Введите имя:', message, state)


async def processFirstName(message: types.Message, state: FSMContext):
    await string_validation(message.text, 'firstName', 'Введите отчество:', message, state)


async def processMiddleName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['middleName'] = message.text.lower()
    await message.answer(fio(data.as_dict()), reply_markup=marcup)
    await state.finish()


@dp.callback_query_handler(Text(startswith="Yes"))
async def processCorrectAnswer(callback_query: CallbackQuery):

    await sqile_db.sql_check_user(storage)
    await callback_query.answer()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(processSecondName, state=Form.secondName)
    dp.register_message_handler(processFirstName, state=Form.firstName)
    dp.register_message_handler(processMiddleName, state=Form.middleName)

