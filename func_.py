from dispatcher import bot
from database import User


async def send_msg_and_btns(telegram_id, text_uz, text_en, btn_uz, btn_en):
    if not await User.get_lang(telegram_id) == 'uz':
        await bot.send_message(telegram_id, text_en, reply_markup=btn_en)
    else:
        await bot.send_message(telegram_id, text_uz, reply_markup=btn_uz)


async def send_msg(telegram_id, text_uz, text_en):
    if await User.get_lang(telegram_id) == 'en':
        await bot.send_message(telegram_id, text_en)
    else:
        await bot.send_message(telegram_id, text_uz)
