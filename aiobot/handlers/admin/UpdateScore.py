from aiogram.dispatcher import FSMContext

from aiobot.buttons import admin_panel_uz, admin_panel_en
from dispatcher import dis
from func_ import send_msg_and_btns, del_msg, send_msg
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiobot.models import User

from states import Update_money


@dis.callback_query_handler(text=['add money'])
async def update_score_1(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg(user_id, 'Qancha ball qoshilsin', 'How many points should be added')
    await Update_money.HoeManyPoints.set()


@dis.message_handler(state=Update_money.HoeManyPoints)
async def update_score_2(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        score = await User.get(user_id)
        for i in score:
            data['HoeManyPoints'] = i.score + int(msg.text)
            await send_msg(user_id, 'Userni hisob raqamini jo\'naintg', 'Send user account number')
            await Update_money.ToWhom.set()


@dis.message_handler(state=Update_money.ToWhom)
async def update_score_3(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        kwargs = {
            'score': data.get('HoeManyPoints'),
        }
        await User.update(msg.text, **kwargs)
        await send_msg_and_btns(user_id, 'Qo\'shildi', 'Added', admin_panel_uz(), admin_panel_en())
    await state.finish()