from dispatcher import dis
from aiobot.buttons import menu_en, menu_uz
from func_ import send_msg_and_btns, del_msg
from aiogram.types import CallbackQuery


@dis.callback_query_handler(text=['Top up the account'])
async def add_money(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    # await send_msg_and_btns(user_id, f'Adminni lichkasiya yozing\n@HamidIsomov\n@Ibr6xim\n\nSizni hisob raqamingiz: {user_id}',f'Write admin \n@HamidIsomov\n@Ibr6xim\n\nYour account number: {user_id}', menu_uz(),menu_en())
    await send_msg_and_btns(user_id,
                            f'Adminni lichkasiya yozing\n@HamidIsomov\n@Ibr6xim\n\nSizni hisob raqamingiz: {user_id}',
                            f'Write admin \n@HamidIsomov\n@Ibr6xim\n\nYour account number: {user_id}', menu_uz(),
                            menu_en())
