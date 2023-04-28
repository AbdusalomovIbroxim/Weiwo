from aiogram.types import CallbackQuery
from aiobot.buttons import my_cabinet_uz, my_cabinet_en
from dispatcher import dis
from func_ import send_msg_and_btns, del_msg


@dis.callback_query_handler(text=['My cabinet'])
async def MyCabinet(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg_and_btns(user_id, 'Mening kobinetm', 'My cabinet', my_cabinet_uz(), my_cabinet_en())
