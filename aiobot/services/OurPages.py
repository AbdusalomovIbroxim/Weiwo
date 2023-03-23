from aiobot.buttons import menu_uz, menu_en
from dispatcher import dis
from aiogram.types import CallbackQuery
from func_ import del_msg, send_msg_and_btns


@dis.callback_query_handler(text=['Our pages'])
async def our_pages(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg_and_btns(user_id, f'@tecnoprom\n@siryo\n@uskunabu\n@siryouzb',
                            f'@tecnoprom\n@siryo\n@uskunabu\n@siryouzb', menu_uz(), menu_en())
