from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


marcup = InlineKeyboardMarkup(row_width=2)
buttonYes = InlineKeyboardButton(text="Yes", callback_data="Yes")
buttonNo = InlineKeyboardButton(text="No", callback_data="No")
marcup.add(buttonYes, buttonNo)
