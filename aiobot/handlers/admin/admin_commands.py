from dispatcher import dis  # bot
from aiogram.types import Message


@dis.message_handler(commands=['MeNewAdmin'])
async def new_admin(msg: Message):
    ...
