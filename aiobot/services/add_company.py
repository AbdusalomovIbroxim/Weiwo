from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiobot.buttons import YesOrNo, menu_en, menu_uz, sub_category_uz, \
    sub_category_en, category_en, category_uz, regions_uz
from aiobot.buttons.inline import regions_buttons_uz, regions_buttons_en
from aiobot.models import User, Product
from dispatcher import dis, bot
from func_ import send_msg_and_btns, send_msg, del_msg
from states import AddCompany


@dis.callback_query_handler(text='Add company')
async def start_add_company(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    if not await User.check_admin(user_id) == 'admin':
        if await User.get_lang(user_id) == 'uz':
            await bot.send_photo(user_id, open('media/img.png', 'rb'), caption="*Siz admin emassiz*",
                                 parse_mode='markdown')
        else:
            await bot.send_photo(user_id, open('media/img_1.png', 'rb'), caption="*You are not an admin*",
                                 parse_mode='markdown')
    else:
        await send_msg_and_btns(user_id, "Tanlang", "Choose", regions_buttons_uz(), regions_buttons_en())
        await AddCompany.city.set()


@dis.callback_query_handler(state=AddCompany.city)
async def input_city(call: CallbackQuery, state: FSMContext):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    async with state.proxy() as data:
        region_id = call.data.split('region_')[-1]
        data['city'] = regions_uz.get(region_id)
        await send_msg(user_id, "Kompaniya nomini jo'nating", "Send company name")
        await AddCompany.name.set()


@dis.message_handler(state=AddCompany.name)
async def input_name(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
        user_id = str(msg.from_user.id)
        await del_msg(user_id, msg.message_id, 2)
        await send_msg_and_btns(user_id, 'Tanlang', 'Choose category', category_uz(), category_en())
    await AddCompany.category.set()


@dis.callback_query_handler(state=AddCompany.category)
async def input_category(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = call.data[8:]
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 1)
        await send_msg_and_btns(user_id, 'Tanlang', 'Choose', sub_category_uz(), sub_category_en())
        await AddCompany.sub_category.set()


@dis.callback_query_handler(state=AddCompany.sub_category)
async def add_company_input_category(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        data['sub_category'] = call.data[12:]
        # if call.data[12:] != 'Next':
        #     await bot.send_message(user_id, 'Select sub_categories and click next')
        #     if data.get('sub_category') is None:
        #         data['sub_category'] = call.data[12:]
        #         await del_msg(user_id, call.message.message_id, 1)
        #     else:
        #         await del_msg(user_id, call.message.message_id, 2)
        #         data['sub_category'] = data.get('sub_category') + " " + call.data[12:]
        #     await send_msg_and_btns(user_id, "Tanlang", "Choose", sub_category_uz(), sub_category_en())
        # elif call.data[12:] == 'Next':
    await del_msg(user_id, call.message.message_id, 1)
    await send_msg(user_id, "Yandex url jo'nating", "Send Yandex maps url")
    await AddCompany.yandex_maps_url.set()


@dis.message_handler(state=AddCompany.yandex_maps_url)
async def input_yandex_maps_url(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        if msg.text.startswith('https://yandex.uz/maps/'):
            data['yandex_maps_url'] = msg.text
            await send_msg(user_id, "Rasm + ma'lumot jo'nating'", 'Send photo + description')
            await del_msg(user_id, msg.message_id, 2)
            await AddCompany.photo.set()
        else:
            await send_msg(user_id, "Url da hatolik qaytatdan jo'nating", "Resend url error in url")
            await del_msg(user_id, msg.message_id, 1)
            await AddCompany.yandex_maps_url.set()


@dis.message_handler(content_types=['photo'], state=AddCompany.photo)
async def input_photo(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        data['photo'] = msg.photo[0].file_id
        data['description'] = msg.caption
        await del_msg(user_id, msg.message_id, 2)
        if msg.caption is None:
            await send_msg(user_id, "ma'lumot jo'nating", "Send description")
            await AddCompany.description.set()
        else:
            await bot.send_photo(user_id, data.get('photo'),
                                 caption=f"{data.get('description')}\n\n📍{data.get('city')}\n\n#{data.get('category')} #{data.get('sub_category')}\n\n{data.get('name')}")
            await send_msg_and_btns(user_id, "Hammasi tog'rimi ?", "All success ?", YesOrNo(), YesOrNo())
            await AddCompany.explanation.set()


@dis.message_handler(state=AddCompany.description)
async def input_description(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        await del_msg(user_id, msg.message_id, 1)
        data['description'] = msg.text
        await bot.send_photo(user_id, data.get('photo'),
                             caption=f"{data.get('description')}\n\n📍{data.get('city')}\n\n#{data.get('category')} #{data.get('sub_category')}\n\n{data.get('name')}")
        await bot.send_message(user_id, data.get('yandex_maps_url'))
        await send_msg_and_btns(user_id, "Hammasi tog'rimi ?", "All success ?", YesOrNo(), YesOrNo())
    await AddCompany.explanation.set()


@dis.callback_query_handler(state=AddCompany.explanation)
async def success(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        if call.data == 'yes':
            data = {
                "full_name": call.from_user.full_name,
                "city": data.get('city'),
                "name": data.get('name'),
                "category": data.get('category'),
                "sub_category": data.get('sub_category'),
                "yandex_maps_url": data.get('yandex_maps_url'),
                "photo": data.get('photo'),
                "description": data.get('description'),
            }
            await Product.add_product(user_id, **data)
            await del_msg(user_id, call.message.message_id, 2)
            await send_msg_and_btns(user_id, "Qo'shildi ✅", "Added ✅", menu_uz(), menu_en())
        else:
            await AddCompany.city.set()
    await state.finish()
