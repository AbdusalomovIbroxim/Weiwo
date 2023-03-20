from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from states import Application
from dispatcher import dis, bot
from aiobot.buttons import application_menu_en, application_menu_uz, application_category_en, application_category_uz, \
    application_sub_category_uz, application_sub_category_en, YesOrNo, menu_uz, menu_en
from func_ import send_msg_and_btns, send_msg, del_msg


@dis.callback_query_handler(text='Application')
async def start_add_anouncement(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg_and_btns(user_id, "Menu", "Menu", application_menu_uz(), application_menu_en())
    await Application.type.set()


@dis.callback_query_handler(text=['Selling', 'Searching', 'Main menu', 'All application'], state=Application.type)
async def add_application(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == 'All application':
            await bot.send_photo(call.from_user.id, photo=open('media/PageNotFound.png', 'rb'))
        else:
            user_id = str(call.from_user.id)
            await del_msg(user_id, call.message.message_id, 1)
            print(call.data)
            if call.data == 'Main menu':
                await send_msg_and_btns(user_id, "Menu", "Menu", menu_uz(), menu_en())
                await state.finish()
            else:
                data['type'] = call.data.lower()
                await send_msg(user_id, "Telefon raqamingizni jo'nating",
                               "Send phone number")
                await Application.contact.set()


@dis.message_handler(state=Application.contact)
async def add_contact(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        # if msg.content_type == 'contact':
        #     data['contact'] = msg.contact.phone_number
        # elif msg.content_type == 'text':
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
            await bot.send_photo('@TESt_my_bo', data.get('photo'),
                                 caption=f"{data.get('description')}\n\n#{data.get('category')} #{data.get('sub_category')}\n\n{data.get('contact')}\n@{call.from_user.username}")
            await send_msg_and_btns(user_id, "Jo'natildi ✅", 'Added ✅', menu_uz(), menu_en())
        elif call.data == 'no':
            await send_msg_and_btns(str(call.from_user.id), "Menu", "Menu", menu_uz(),
                                    menu_en())
        await state.finish()

# @dis.callback_query_handler(text=['All application'])
# async def send_all_applications(call: CallbackQuery):
