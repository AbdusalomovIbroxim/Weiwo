from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiobot.buttons import chooce_lang, phone, menu_uz
from aiobot.models import User
from aiobot.buttons import menu_en
from dispatcher import dis
from func_ import send_msg_and_btns, del_msg
from states import CreateAccount


@dis.message_handler(commands=['start'], state=['*'])
async def send_welcome(msg: Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if not await User.get(user_id):
        await msg.answer("*Choose lanuage:\n"
                         "----------\n"
                         "Tilni tanlang:*", parse_mode='markdown', reply_markup=chooce_lang())
        await CreateAccount.lang.set()
    else:
        # await del_msg(user_id, msg.message_id, 1)
        await send_msg_and_btns(user_id, 'Menu', 'Menu', menu_uz(), menu_en())
    await state.finish()


@dis.callback_query_handler(text=['uz', 'en'], state=CreateAccount.lang)
async def input_lang(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['lang'] = call.data
        await call.message.answer("*Click button   -|:\n"
                                  "     \n"
                                  "Tugmasini bosing-|:*", parse_mode='markdown',
                                  reply_markup=phone())
        await CreateAccount.phone_number.set()


@dis.message_handler(content_types='contact', state=CreateAccount.phone_number)
async def input_contact(msg: Message, state: FSMContext):
    async with state.proxy() as s:
        user_id = str(msg.from_user.id)
        s['phone_number'] = msg.contact.phone_number
        data = {
            "phone_number": s.get('phone_number'),
            "full_name": msg.from_user.full_name,
            'lang': s.get('lang')
        }
        await User.create(user_id, **data)
        await send_msg_and_btns(user_id, 'Yaratildi', 'Created', menu_uz(), menu_en())
    await state.finish()
