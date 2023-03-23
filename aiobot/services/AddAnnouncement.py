from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from states import Application
from dispatcher import dis, bot
from aiobot.buttons import application_menu_en, application_menu_uz, application_category_en, application_category_uz, \
    application_sub_category_uz, application_sub_category_en, YesOrNo, menu_uz, menu_en
from func_ import send_msg_and_btns, send_msg, del_msg
from aiobot.models.user import User
from aiobot.models import Announcement


@dis.callback_query_handler(text='Application')
async def start_add_anouncement(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg_and_btns(user_id, "Menu", "Menu", application_menu_uz(), application_menu_en())
    await Application.type.set()


@dis.callback_query_handler(text=['Selling', 'Searching', 'Main menu', 'All application'], state=Application.type)
async def add_application(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 1)
        if call.data == 'Main menu':
            await send_msg_and_btns(user_id, "Menu", "Menu", menu_uz(), menu_en())
            await state.finish()
        elif call.data == 'All application':
            await bot.send_photo(user_id, open('media/PageNotFound.png', 'rb'))
            await send_msg_and_btns(user_id, "Hali ishga tushurilmagan", 'Page not found', application_menu_uz(),
                                    application_menu_en())
        else:
            data['type'] = call.data.lower()
            await send_msg_and_btns(user_id, 'Kategoriyalar', 'Categories', application_category_uz(),
                                    application_category_en())
            await Application.category.set()


@dis.message_handler(state=Application.contact)
async def add_contact(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        await del_msg(user_id, msg.message_id, 2)
        if msg.text.startswith('+998') or msg.text.startswith('998') and msg.text[1:].isnumeric():
            data['contact'] = msg.text
            await send_msg_and_btns(user_id, 'Kategoriyalar', 'Categories', application_category_uz(),
                                    application_category_en())
            await Application.category.set()


@dis.callback_query_handler(state=Application.category)
async def add_category(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        data['contact'] = await User.tell(user_id)
        print(data.get('contact'))
        data['category'] = call.data
        await del_msg(user_id, call.message.message_id, 1)
        await send_msg_and_btns(user_id, 'Sub category', 'Sub category', application_sub_category_uz(),
                                application_sub_category_en())
        await Application.sub_category.set()


@dis.callback_query_handler(state=Application.sub_category)
async def add_sub_category(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['sub_category'] = call.data
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 1)
        await send_msg(user_id, "Rasm va ma'lumot qoldiring", "Send photo and description")
        await Application.description.set()


@dis.message_handler(state=Application.description, content_types='photo')
async def add_description(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = msg.photo[0].file_id
        data['description'] = msg.caption
        user_id = str(msg.from_user.id)
        await del_msg(user_id, msg.message_id, 2)
        await Application.photo.set()
        await bot.send_photo(str(msg.from_user.id), data.get('photo'),
                             caption=f"📂 {data.get('description')}\n\n#{data.get('category')} #{data.get('sub_category')}\n\n☎ {data.get('contact')}\n\n👤 @{msg.from_user.username}",
                             reply_markup=YesOrNo(), parse_mode='markdown')
    await Application.username.set()


@dis.callback_query_handler(state=Application.username)
async def add_description(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 1)
        if call.data == 'yes':
            kwargs = {
                "type": data.get('type'),
                "phone_number": data.get('contact'),
                "photo": data.get('photo'),
                "description": data.get('description'),
                "category": data.get('category'),
                "sub_category": data.get('sub_category')
            }
            await Announcement.add(user_id, **kwargs)
            await bot.send_photo('@Weiwo_project', data.get('photo'),
                                 caption=f"{data.get('description')}\n\n#{data.get('category')} #{data.get('sub_category')}\n\n{data.get('contact')}\n@{call.from_user.username}")
            await send_msg_and_btns(user_id, "Jo'natildi ✅", 'Added ✅', menu_uz(), menu_en())
        elif call.data == 'no':
            await send_msg_and_btns(str(call.from_user.id), "Menu", "Menu", menu_uz(),
                                    menu_en())
        await state.finish()
