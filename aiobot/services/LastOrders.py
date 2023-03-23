from dispatcher import dis, bot
from aiogram.types import CallbackQuery
from aiobot.models import Announcement


@dis.callback_query_handler(text='Last orders')
async def last_orders(call: CallbackQuery):
    a = await Announcement.get()
    for i in a:
        await bot.send_photo(call.from_user.id, i[0].photo, i[0].description)
