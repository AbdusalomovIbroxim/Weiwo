from aiogram.types import CallbackQuery
from dispatcher import dis, bot
from func_ import del_msg


@dis.callback_query_handler(text='Our pages')
async def our_pages(call: CallbackQuery):
    user_id = str(call.from_user.id)
    await del_msg(user_id, call.message.message_id, 1)
    await bot.send_photo(user_id, open('media/OurPage.jpg', 'rb'),
                         '@tecnoprom\n@siryo\n@uskunabu\n@siryouzb\n@tecnoprom\n@siryo\n@uskunabu\n@siryouzb')
