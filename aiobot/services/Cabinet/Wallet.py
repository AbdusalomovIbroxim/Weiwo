from aiobot.buttons import menu_uz, menu_en
from dispatcher import dis
from aiogram.types import CallbackQuery
from aiobot.models import User
from func_ import send_msg_and_btns, del_msg


@dis.callback_query_handler(text=['Wallet'])
async def test(call: CallbackQuery):
    user_id = str(call.from_user.id)
    wallet = await User.get(user_id)
    await del_msg(user_id, call.message.message_id, 1)
    for i in wallet:
        await send_msg_and_btns(user_id, f'💳 {i.score}', f'💳 {i.score}', menu_uz(), menu_en())
