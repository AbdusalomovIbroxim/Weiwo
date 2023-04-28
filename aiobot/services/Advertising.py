from aiogram.dispatcher import FSMContext

from aiobot.models import User
from aiobot.buttons import menu_uz, menu_en, YesOrNo
from dispatcher import dis, bot
from aiogram.types import CallbackQuery, Message

from func_ import send_msg, send_msg_and_btns, del_msg
from states import Advertising


@dis.callback_query_handler(text='Weakness to join the company')
async def advertising(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg(user_id,
                   "Rasm + text jo'nating yoki textni o'zini jo'nating\n\nMisol\n🌆Rasm\n📂Ma'lumot",
                   "Send photo+text or only text \n\n Example:\n🌆Photo\n📂Description")
    await Advertising.photo.set()


@dis.message_handler(content_types=['any'], state=Advertising.photo)
async def advertising_photo_plus_text(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        if msg.text == '/start':
            await send_msg_and_btns(user_id, "Reklama adminga jo'natildi", 'Menu', menu_uz(), menu_en())
            await state.finish()

        phone = await User.get(user_id)
        for i in phone:
            data['phone'] = i.phone_number
        if msg.content_type == 'photo' and msg.caption is not None:
            data['photo'] = msg.photo[0].file_id
            data['description'] = msg.caption
            await del_msg(user_id, msg.message_id, 2)
            await bot.send_photo(user_id, data.get('photo'), f"{data.get('description')}\n\n☎ {data.get('phone')}")
            await send_msg_and_btns(user_id, "Hammasi tog'rimi ?", "All success ?", YesOrNo(), YesOrNo())
            await Advertising.description.set()
        elif msg.content_type == 'text' and msg.text != '/start':
            data['description'] = msg.caption
            await bot.send_message(user_id, f'{msg.text}\n\n☎ {data.get("phone")}')
            await del_msg(user_id, msg.message_id, 2)
            await send_msg_and_btns(user_id, "Hammasi tog'rimi ?", "All success ?", YesOrNo(), YesOrNo())
            await Advertising.description.set()


@dis.callback_query_handler(text=['yes', 'no'], state=Advertising.description)
async def advertising_yes_or_no(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 2)
        if call.data == 'yes':
            if data.get('photo'):
                await bot.send_photo('@Weiwo_project_2', data.get('photo'),
                                     f"{data.get('description')}\n\n☎ {data.get('phone')}")
                await send_msg_and_btns(user_id, "Reklama adminga jo'natildi",
                                        "Announcement sent to administrator",
                                        menu_uz(), menu_en())
            else:
                await bot.send_message('@Weiwo_project_2', f"{data.get('description')}\n\n☎ {data.get('phone')}")
                await send_msg_and_btns(user_id, "Reklama adminga jo'natildi",
                                        "Announcement sent to administrator",
                                        menu_uz(), menu_en())
        elif call.data == 'no':
            await send_msg_and_btns(user_id, "Menu",
                                    "Menu",
                                    menu_uz(), menu_en())
    await state.finish()
