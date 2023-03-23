from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from aiobot.buttons import my_cabinet_uz, my_cabinet_en, category_uz, category_en, sub_category_uz, sub_category_en, \
    my_announcements, YesOrNo
from dispatcher import dis
from func_ import send_msg_and_btns, send_msg, del_msg
from states import Edit_announcement
from aiobot.models import Announcement, Company


@dis.callback_query_handler(text=['My cabinet'])
async def MyCabinet(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg_and_btns(user_id, 'Mening kobinetm', 'My cabinet', my_cabinet_uz(), my_cabinet_en())

