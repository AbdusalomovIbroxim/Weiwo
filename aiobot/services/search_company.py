from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiobot.buttons import sub_category_uz, sub_category_en, category_en, category_uz, regions_uz, get_rating_buttons, \
    btn_comp, menu_en, menu_uz
from aiobot.buttons.inline import regions_buttons_uz, regions_buttons_en
from database import User, Product
from database.models.rating import UserInCompany
from dispatcher import dis, bot
from func_ import send_msg_and_btns
from states import SearchCompany


@dis.callback_query_handler(text='Search company')
async def search_company(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await send_msg_and_btns(user_id, 'Tanlang - search', 'Choose - search', regions_buttons_uz(), regions_buttons_en())
    await SearchCompany.city.set()


@dis.callback_query_handler(state=SearchCompany.city)
async def search_input_city(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        region_id = call.data.split('region_')[-1]
        data['city'] = regions_uz.get(region_id)
        await send_msg_and_btns(user_id, 'Tanlang', 'Choose category', category_uz(), category_en())
        await SearchCompany.category.set()


@dis.callback_query_handler(state=SearchCompany.category)
async def search_input_category(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        data['category'] = call.data[8:]
    await send_msg_and_btns(user_id, 'Tanlang', 'Choose category - search', sub_category_uz(), sub_category_en())
    await SearchCompany.sub_category.set()


@dis.callback_query_handler(state=SearchCompany.sub_category)
async def search_input_sub_category(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        data['sub_category'] = call.data[12:]
        names = [i[0] for i in
                 await Product.get_company_names(data.get('city'), data.get('category'), data.get('sub_category'))]
        if not names:
            await send_msg_and_btns(user_id, 'Kompaniya topilmadi', 'Company not found', menu_uz(), menu_en())
            await state.finish()
        else:
            await bot.send_message(user_id, f"{names}", reply_markup=btn_comp(names))
            await SearchCompany.name.set()


@dis.callback_query_handler(state=SearchCompany.name)
async def search_end(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        data['name'] = call.data
        company = await Product.get_company(data.get('name'))
        for row in company:
            await bot.send_photo(user_id, row.photo, row.description)
            await bot.send_message(user_id, f'{row.yandex_maps_url}', reply_markup=await get_rating_buttons(row.pk))
    await state.finish()


@dis.callback_query_handler(Text(startswith=['w_', 'p_']))
async def add_staff(call: CallbackQuery):
    user_id = str(call.from_user.id)
    company_id = int(call.data[2:])
    type_conf = {'w': 'worked', 'p': 'partner'}
    if await UserInCompany.is_staff(user_id, company_id):
        if await User.get_lang(user_id) == 'uz':
            text = 'Siz avval bosgansiz ‼'
        else:
            text = 'You clicked first ‼'
        await call.answer(text, show_alert=True)
    else:
        data = {
            "telegram_id": user_id,
            "company_id": company_id,
            "type": call.data[0]
        }
        await UserInCompany.add_staff_(**data)
        text = f'Siz {type_conf[call.data[0]].capitalize()} ni bosdiz'
        await call.answer(text)
        await call.message.edit_text(call.message.text,
                                     reply_markup=await get_rating_buttons(company_id))
