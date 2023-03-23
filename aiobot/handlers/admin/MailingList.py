from aiogram.dispatcher import FSMContext
from aiobot.models import User
from dispatcher import dis, bot
from states import Admin_state
from aiogram.types import Message


@dis.message_handler(state=Admin_state.mailing_list, content_types=['any'])
async def MailingList(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        for id in await User.get_all():
            if msg.content_type == 'photo':
                await bot.send_photo(id[0].user_id, msg.photo[0].file_id, msg.caption)
            elif msg.content_type == 'text':
                await bot.send_photo(id[0].user_id, msg.text)
