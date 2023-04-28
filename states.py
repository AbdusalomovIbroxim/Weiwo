from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateAccount(StatesGroup):
    lang = State()
    phone_number = State()


class AddCompany(StatesGroup):
    telegram_id = State()
    full_name = State()
    city = State()
    name = State()
    category = State()
    sub_category = State()
    photo = State()
    description = State()
    explanation = State()
    yandex_maps_url = State()


class SearchCompany(StatesGroup):
    city = State()
    category = State()
    sub_category = State()
    name = State()


class Application(StatesGroup):
    type = State()
    contact = State()
    category = State()
    sub_category = State()
    description = State()
    photo = State()
    username = State()


class Del(StatesGroup):
    id = State()


class Admin_state(StatesGroup):
    mailing_list = State()
    id = State()
    photo = State()
    description = State()


class Advertising(StatesGroup):
    photo = State()
    description = State()
    phone = State()


class Edit_announcement(StatesGroup):
    id = State()
    type = State()
    category = State()
    sub_category = State()
    photo = State()
    description = State()
    phone = State()
    score = State()


class Update_money(StatesGroup):
    HoeManyPoints = State()
    ToWhom = State()


class AddAdmin(StatesGroup):
    id = State()
