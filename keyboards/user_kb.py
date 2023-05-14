from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


marcup = InlineKeyboardMarkup(row_width=2)
buttonYes = InlineKeyboardButton(text="Yes", callback_data="Yes")
buttonNo = InlineKeyboardButton(text="No", callback_data="No")
marcup.add(buttonYes, buttonNo)


marcup2 = InlineKeyboardMarkup(row_width=3)

buttonTin = InlineKeyboardButton(text="Тинькофф", callback_data="Tinokoff")
buttonRen = InlineKeyboardButton(text="Ренессанс Кредит", callback_data="Renessasns")
buttonSber = InlineKeyboardButton(text="СберБанк", callback_data="Sberbank")
marcup2.add(buttonTin, buttonRen, buttonSber)
