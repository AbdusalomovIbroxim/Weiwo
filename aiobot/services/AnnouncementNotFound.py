from aiobot.buttons import menu_uz, menu_en
from dispatcher import dis
from aiogram.types import CallbackQuery
from func_ import send_msg_and_btns, del_msg


@dis.callback_query_handler(text=['I\'m looking'])
async def page_not_founds(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg_and_btns(user_id, 'Sahifa topilmadi', 'Pane not found', menu_uz(),
                            menu_en())
