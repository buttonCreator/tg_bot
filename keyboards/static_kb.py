from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton('/Информация_по_картам')
b2 = KeyboardButton('/Раздел_\"Кредиты\"')
b3 = KeyboardButton('/Контакты_для_связи_с_банком')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1, b2, b3)


