from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def phone():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    return markup.add(*[KeyboardButton('☎', request_contact=True)])
