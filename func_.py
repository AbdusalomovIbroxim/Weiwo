from dispatcher import bot
from aiobot.models import User


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


async def del_msg(telegram_id: str, msg_id: int, who: int) -> None:
    for i in range(who):
        await bot.delete_message(telegram_id, msg_id - i)
