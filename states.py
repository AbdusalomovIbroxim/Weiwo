from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateAccount(StatesGroup):
    lang = State()
    phone_number = State()


class AddCompany(StatesGroup):
    telegram_id = State()
    full_name = State()
    city = State()
    category = State()
    sub_category = State()
    name = State()
    yandex_maps_url = State()
    photo = State()
    description = State()
    explanation = State()


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