from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv
from database.models import UserInCompany


def read_csv(file_name):
    file = open(file_name)
    file.readline()
    return csv.reader(file)


regions_uz = {_id: name for _id, name in read_csv('regions.csv')}
regions_en = {_id: name for _id, name in read_csv('regions_en.csv')}

text_menu_en = ["Add company", "Advertising",
                "Search company", "I'm looking",
                "Last orders", "Our pages"
                ]
text_menu_uz = ["Kompaniya qo'shish", "Reklama berish",
                "Kompaniya qidirish", "Qidiryapman",
                "Oxirgi buyurtmanlar", "Bizning sahifalar"
                ]
categories_uz_for_s = ['Ishlab chiqaruvchi', "Uskuna ta'minotchi", "Xom ashyo ta'minotchi",
                       "Shahardagi hammam kompaniyalar"]
categories_en_for_s = ["Manufacturer", "Equipment supplier", "Supplier of raw materials", "All companies in city"]
categories_uz_ = ['Ishlab chiqaruvchi', "Uskuna ta'minotchi", "Xom ashyo ta'minotchi"]
categories_en_ = ["Manufacturer", "Equipment supplier", "Supplier of raw materials"]

sub_categories_uz = ['Hammasi',
                     "Umumiy turdagi uskuna ta'minotchisi",
                     'Plastmassa va qarton',
                     'Tekstil/yengil sanoat',
                     'Agro',
                     'Metall',
                     'Qadoqlash/fasovka/markirovka/pechat',
                     'Sanoat iqlim uskunalari',
                     'Ombor uskunalari',
                     'Keyingisi'
                     ]
sub_categories_en = ['Everything',
                     'General equipment supplier',
                     'Plastic and resin',
                     'Textile/light industry',
                     'Agro',
                     'Metal',
                     'Packing/marking/printing',
                     'Industrial climate equipment',
                     'Warehouse equipment',
                     'Next']


def chooce_lang():
    markup = [
        InlineKeyboardButton(
            "🇺🇿Uz", callback_data='uz'
        ),
        InlineKeyboardButton(
            "🇺🇸En", callback_data='en'
        )
    ]
    return InlineKeyboardMarkup().add(*markup)


def menu_uz():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f'{text_menu_en[text_menu_uz.index(text)]}') for text in text_menu_uz
    ]
    return markup.add(*result)


def menu_en():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=text) for text in text_menu_en
    ]
    return markup.add(*result)


def regions_buttons_uz():
    rkm = InlineKeyboardMarkup(row_width=3)
    rkm.add(*[InlineKeyboardButton(name, callback_data=f'region_{_id}') for _id, name in regions_uz.items()])
    return rkm


def regions_buttons_en():
    rkm = InlineKeyboardMarkup(row_width=3)
    rkm.add(*[InlineKeyboardButton(name, callback_data=f'region_{_id}') for _id, name in regions_en.items()])
    return rkm


def category_uz():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f'category{categories_en_[categories_uz_.index(text)]}') for text in
        categories_uz_
    ]
    return markup.add(*result)


def category_en():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f'category{text}') for text in categories_en_
    ]
    return markup.add(*result)


def sub_category_uz():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f'sub_category{sub_categories_en[sub_categories_uz.index(text)]}')
        for text in sub_categories_uz
    ]
    return markup.add(*result)


def sub_category_en():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f'sub_category{text}') for text in sub_categories_en
    ]
    return markup.add(*result)


def YesOrNo():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton("Yes ✅", callback_data='yes'),
        InlineKeyboardButton("No 🚫", callback_data='no')
    ]
    return markup.add(*result)


def btn_comp(result):
    rkm = InlineKeyboardMarkup(row_width=2)
    btns = [
        InlineKeyboardButton(name, callback_data=name) for name in result
    ]
    return rkm.add(*btns)


async def get_rating_buttons(company_id):
    worked = 0 if UserInCompany.staff_list(company_id, "worked") is None else UserInCompany.staff_list(company_id)
    partner = 0 if UserInCompany.staff_list(company_id, "partner") is None else UserInCompany.staff_list(company_id)
    rating_buttons = [
        InlineKeyboardButton(
            f'I worked - {worked}', callback_data=f'w_{company_id}'
        ),
        InlineKeyboardButton(
            f'I\'m a partner - {partner}', callback_data=f'p_{company_id}'
        )
    ]
    return InlineKeyboardMarkup().add(*rating_buttons)
