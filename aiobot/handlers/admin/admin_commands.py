# Todo: Rassilka
# Todo: Add admin
# Todo: Edit company
# Todo: Edit app..
# Todo: del all company and app. (id)
from aiogram.types import Message, CallbackQuery

from aiobot.buttons import menu_uz, menu_en
from aiobot.buttons import admin_panel_uz, admin_panel_en
from dispatcher import dis, bot
from func_ import send_msg_and_btns, send_msg
from aiobot.models import User
from states import Admin_state


@dis.message_handler(commands=['admin'])
async def admin_panel(msg: Message):
    user_id = str(msg.from_user.id)
    status = await User.get(user_id)
    if status[0].status == 'admin':
        await send_msg_and_btns(user_id, '💻 Admin panel', '💻 Admin panel', admin_panel_uz(), admin_panel_en())
    else:
        await bot.send_photo(user_id, open('media/PageNotFound.png', 'rb'))
        await send_msg_and_btns(user_id, 'Hatolik', "Page not found", menu_uz(), menu_en())


@dis.callback_query_handler(text=['Edit company', 'Edit post', 'Del company', 'Del post', 'Newsletter', 'Add admin', 'Mailing list'])
async def delete_company(call: CallbackQuery):
    user_id = str(call.from_user.id)
    if call.data == 'Mailing list':
        await send_msg(user_id, "Jo'nating", 'Send message')
        await Admin_state.mailing_list.set()
    else:
        await bot.send_photo(user_id, open('media/PageNotFound.png', 'rb'))
        await send_msg_and_btns(user_id, 'Hatolik', "Page not found", admin_panel_uz(), admin_panel_en())
