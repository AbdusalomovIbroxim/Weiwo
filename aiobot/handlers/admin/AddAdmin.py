from aiogram.dispatcher import FSMContext

from aiobot.buttons import admin_panel_uz, admin_panel_en
from dispatcher import dis
from func_ import send_msg_and_btns, del_msg, send_msg
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiobot.models import User

from states import AddAdmin


@dis.callback_query_handler(text=['Add admin'])
async def update_score_1(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg(user_id, 'Userni hisob raqamini kiriting', 'Send user account number')
    await AddAdmin.id.set()


@dis.message_handler(state=AddAdmin.id)
async def update_score_2(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        await User.update(msg.text, **{'status': 'admin'})
        await send_msg_and_btns(user_id, 'Status o\'gartirildi', 'Status updated', admin_panel_uz(), admin_panel_en())
    await state.finish()
