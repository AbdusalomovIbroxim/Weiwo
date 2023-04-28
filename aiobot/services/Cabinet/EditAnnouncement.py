from aiogram.dispatcher import FSMContext

from dispatcher import dis, bot
from aiogram.types import CallbackQuery, Message
from func_ import del_msg, send_msg, send_msg_and_btns
from aiobot.buttons import my_announcements, YesOrNo, my_cabinet_uz, my_cabinet_en, application_category_uz, \
    application_category_en, application_sub_category_uz, application_sub_category_en, application_menu_uz, \
    application_menu_en  # menu_en, menu_uz
from states import Edit_announcement
from aiobot.models import Announcement, User


@dis.callback_query_handler(text=['Edit announcement'])
async def ides(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    # await send_msg_and_btns(user_id, 'Hatolik', "Page not found", menu_uz(), menu_en())
    await send_msg_and_btns(user_id, 'qaysi birini o\'zgartirasiz', 'Which one will you change',
                            await my_announcements(user_id),
                            await my_announcements(user_id))
    await Edit_announcement.id.set()


@dis.callback_query_handler(state=Edit_announcement.id)
async def edit(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = call.data
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 1)
        await send_msg_and_btns(user_id, 'Tanlang', 'Choose', application_menu_uz(), application_menu_en())
        await Edit_announcement.type.set()


@dis.callback_query_handler(state=Edit_announcement.type)
async def edit(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        if call.data == 'Main menu':
            await del_msg(user_id, call.message.message_id, 1)
            await send_msg_and_btns(user_id, 'Tanlang', 'Choose', application_menu_uz(), application_menu_en())
            await Edit_announcement.type.set()
        else:
            data['type'] = call.data
            await del_msg(user_id, call.message.message_id, 1)
            await send_msg_and_btns(user_id, 'Tanlang', 'Choose', application_category_uz(), application_category_en())
            await Edit_announcement.category.set()


@dis.callback_query_handler(state=Edit_announcement.category)
async def edit(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        data['category'] = call.data
        await del_msg(user_id, call.message.message_id, 1)
        await send_msg_and_btns(user_id, 'Tanlang', 'Choose', application_sub_category_uz(),
                                application_sub_category_en())
        await Edit_announcement.sub_category.set()


@dis.callback_query_handler(state=Edit_announcement.sub_category)
async def edit(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['sub_category'] = call.data
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 1)
        await send_msg(user_id, 'Rasm+text jo\'nating', 'Send  photo and description')
        await Edit_announcement.photo.set()


@dis.message_handler(state=Edit_announcement.photo, content_types=['photo'])
async def edit(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(msg.from_user.id)
        phone = await User.get(user_id)
        for i in phone:
            data['phone'] = i.phone_number
        data['photo'] = msg.photo[0].file_id
        await del_msg(user_id, msg.message_id, 1)
        if msg.caption is None:
            await del_msg(user_id, msg.message_id, 1)
            await send_msg(user_id, 'Ma\'lumot jo\'natong', 'Send description')
            await Edit_announcement.description.set()
        else:
            data['description'] = msg.caption
            await bot.send_photo(user_id, data.get('photo'),
                                 f"{data.get('description')}\n\n{data.get('category')}\n\n{data.get('sub_category')}\n\n{data.get('category')}")
            await send_msg_and_btns(user_id, 'Hammasi tog\'rimi', 'All success', YesOrNo(), YesOrNo())
            await Edit_announcement.score.set()


@dis.message_handler(state=Edit_announcement.description)
async def edit(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = msg.text
        user_id = str(msg.from_user.id)
        await del_msg(user_id, msg.message_id, 1)
        await send_msg_and_btns(user_id, 'Hammasi tog\'rimi', 'All success', YesOrNo(), YesOrNo())
        await Edit_announcement.score.set()


@dis.callback_query_handler(text=['yes', 'no'], state=Edit_announcement.score)
async def yes_no(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = str(call.from_user.id)
        await del_msg(user_id, call.message.message_id, 2)
        edit = {
            'type': data.get('type'),
            'phone_number': data.get('phone'),
            "photo": data.get('photo'),
            "description": data.get('description'),
            "category": data.get('category'),
            "sub_category": data.get('sub_category')
        }
        if call.data == 'yes':
            await Announcement.update(int(data.get('id')), **edit)
            await send_msg_and_btns(user_id, '👍 O\'zgartirildi', '👍 Edited', my_cabinet_uz(), my_cabinet_en())
        elif call.data == 'no':
            await send_msg_and_btns(user_id, 'Mening kobinetm', 'My cabinet', my_cabinet_uz(), my_cabinet_en())
    await state.finish()


"""
user_id
type
phone_number
photo
description
category
sub_category
"""
