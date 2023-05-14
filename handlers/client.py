from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram_datepicker import DatepickerSettings
from create_bot import dp, storage
from keyboards.static_kb import kb_client

from data_base import sqile_db
from keyboards.user_kb import marcup

from keyboards.user_kb import marcup2


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
    await message.answer('Чтобы я мог коректно работать, пожалуйста, авторизируйтесь\n\nВведите фамилию:',
                         reply_markup=ReplyKeyboardRemove())


async def processSecondName(message: types.Message, state: FSMContext):
    await string_validation(message.text, 'secondName', 'Введите имя:', message, state)


async def processFirstName(message: types.Message, state: FSMContext):
    await string_validation(message.text, 'firstName', 'Введите отчество:', message, state)


async def processMiddleName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['middleName'] = message.text.lower()
    await message.answer(fio(data.as_dict()), reply_markup=marcup)
    await state.finish()


async def informationOfCards(message: types.Message):
    await message.answer('''
    СберБанк
    Тип карты: Дебитовая, Номер карты: ..7597, Карта активна
    Баланс: 22945.78

    СберБанк
    Тип карты: Дебитовая, Номер карты: ..0412, Карта активна
    Баланс: 0.6

    СберБанк
    Тип карты: Карта с овердрафтом, Номер карты: ..4376, Карта активна
    Баланс: -22945.78

    Ренесанс Кредит
    Тип карты: Дебитовая, Номер карты: ..8754, Карта заблокирована
    Баланс: 3245676.0

    Общая сумма по картам: 0.5999999999985448
    ''')


async def contactsOfBanks(message: types.Message):
    await message.answer('Выберете Банк', reply_markup=marcup2)


async def contactOfTinkoffBank(message: types.Message):
    await message.answer('''
    Тинькофф Банк
    
    Телефон горячей линии Тинькофф
    8 800 555-777-8
    
    Сайт - https://www.tinkoff.ru/
    ''')


async def contactOfRenessansCredit(message: types.Message):
    await message.answer('''
    Ренессанс Кредит
    
    Электронная почта:
    consultant@rencredit.ru

    Горячая линия для клиентов банка:
    8 (800) 200-09-81бесплатный номер по России

    Головной офис:
    +7 (495) 783-46-00

    Сайт - https://rencredit.ru/
    ''')


async def contactOfCberbank(message: types.Message):
    await message.answer('''
    СберБанк

    С мобильного телефона в России
    По номеру 900

    С мобильного или городского из-за границы
    По номеру +7 495 500-55-50

    Сайт - http://www.sberbank.ru/ru/person
    ''')


async def caseCredit(message: types.Message):
    await message.answer('''
    СберБанк
    Карта с овердрафтом, Номер карты: ..4376, Карта активна
    Сума долга: 22945.78
    Число каждого месяца, для погашения задолжности без процентов: 15
    Иначе процент на задолжность составит 11.0%
    Максимальная сумма заложности не может превышать 50000

    Ренесанс Кредит
    Кредит, Кредит оформлен на 24 месяца, с процентной ставкой: 4.5%
    Ежемесячный платеж: 6498.0 рублей
    ''')


@dp.callback_query_handler(Text(startswith="Yes"))
async def processCorrectAnswer(callback_query: CallbackQuery):
    await callback_query.message.answer('Отлично!', reply_markup=kb_client)
    await callback_query.answer()


@dp.callback_query_handler(Text(startswith="Sberbank"))
async def processGetContactSber(callback_query: CallbackQuery):
    await callback_query.message.answer('''
    СберБанк

    С мобильного телефона в России
    По номеру 900

    С мобильного или городского из-за границы
    По номеру +7 495 500-55-50

    Сайт - http://www.sberbank.ru/ru/person
    ''')
    await callback_query.answer()


@dp.callback_query_handler(Text(startswith="Tinokoff"))
async def processGetContactTinokoff(callback_query: CallbackQuery):
    await callback_query.message.answer('''
    Тинькофф Банк
    
    Телефон горячей линии Тинькофф
    8 800 555-777-8
    
    Сайт - https://www.tinkoff.ru/
    ''')
    await callback_query.answer()


@dp.callback_query_handler(Text(startswith="Renessasns"))
async def processGetContactRenessasns(callback_query: CallbackQuery):
    await callback_query.message.answer('''
    Ренессанс Кредит
    
    Электронная почта:
    consultant@rencredit.ru

    Горячая линия для клиентов банка:
    8 (800) 200-09-81бесплатный номер по России

    Головной офис:
    +7 (495) 783-46-00

    Сайт - https://rencredit.ru/
    ''')
    await callback_query.answer()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(informationOfCards, commands=['Информация_по_картам'])
    dp.register_message_handler(caseCredit, commands=['Раздел_\"Кредиты\"'])
    dp.register_message_handler(contactsOfBanks, commands=['Контакты_для_связи_с_банком'])
    dp.register_message_handler(contactOfTinkoffBank, commands=['Тинькофф'])
    dp.register_message_handler(contactOfRenessansCredit, commands=['Ренессанс_Кредит'])
    dp.register_message_handler(contactOfCberbank, commands=['СберБанк'])
    dp.register_message_handler(processSecondName, state=Form.secondName)
    dp.register_message_handler(processFirstName, state=Form.firstName)
    dp.register_message_handler(processMiddleName, state=Form.middleName)
