from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv

from aiobot.models import Company, Announcement


def read_csv(file_name):
    file = open(file_name)
    file.readline()
    return csv.reader(file)


regions_uz = {_id: name for _id, name in read_csv('regions.csv')}
regions_en = {_id: name for _id, name in read_csv('regions_en.csv')}

text_menu_en = ["Add company", "Weakness to join the company",
                "Search company",
                "Our pages", "Application", 'My cabinet'
                ]  # "Last orders"
text_menu_uz = ["Kompaniya qo'shish", "Kompaniya qoshishga zayafka berish",
                "Kompaniya qidirish",
                "Bizning sahifalar", "Zayavka", 'Mening kablinetm'
                ]  # "Oxirgi buyurtmanlar"
# categories_uz_for_s = ['Ishlab chiqaruvchi', "Uskuna ta'minotchi", "Xom ashyo ta'minotchi",
#                        "Shahardagi hammam kompaniyalar"]
# categories_en_for_s = ["Manufacturer", "Equipment supplier", "Supplier of raw materials", "All companies in city"]
categories_uz_ = ['Ishlab chiqaruvchi', "Uskuna ta'minotchi", "Xom ashyo ta'minotchi"]
categories_en_ = ["Manufacturer", "Equipment supplier", "Supplier of raw materials"]

sub_categories_uz = ["Umumiy turdagi uskuna ta'minotchisi",
                     'Plastmassa',
                     'Tekstil/yengil sanoat',
                     'Agro',
                     'Metall',
                     'Qadoqlash/fasovka/markirovka/pechat',
                     'Sanoat iqlim uskunalari',
                     'Ombor uskunalari',
                     'Oziq ovqat'
                     ]
sub_categories_en = ['General equipment supplier',
                     'Plastic',
                     'Textile/light industry',
                     'Agro',
                     'Metal',
                     'Packing/marking/printing',
                     'Industrial climate equipment',
                     'Warehouse equipment',
                     "Food"]

sub_category_uz_uskuna = [
    "Хаммаси",
    "Умумий турдаги ускунв та'минотчиси",
    "Пластмасса ва ресин",
    "Текстил/енгил саноат",
    "агро",
    "Металл",
    "Қадоқлаш/фасовка/маркировка/печат",
    "Саноат иқлим ускуналари",
    "Омбор ускуналари",
    "Озиқ - овқат ишлаб чиқариш",
    "Кимёвий жараёнлар ускуналари",
    "Энергия ва электр жиҳозлари",
    "Хизмат кўрсатиш",
    "Қурилиш ускуна ва техникалари",
    "Ёғоч ва мебелсозлик",
    "Ёрдамчи ускуналар",
    "Машинасозлик деталлари",
]
sub_category_en_uskuna = [
    "Everything",
    "Generic Equipment Provider",
    "Plastic and resin",
    "Textile/light industry",
    "Agro",
    "Metal",
    "Packing/packaging/marking/printing",
    "Industrial climate equipment",
    "Warehouse equipment",
    "Food production",
    "Chemical process equipment",
    "Energy and electrical equipment",
    "Servicing",
    "Construction equipment and techniques",
    "Wood and furniture",
    "Auxiliary equipment",
    "Mechanical engineering details",
]

application_uz = ["Sotish", "Qidirish", "Barcha e'lonlar", "Asosiy menyuga"]
application_en = ["Selling", "Searching", "All application", "Main menu"]

application_category_uz_text = ['Uskuna', 'Ishlab chiqaruvchi', 'Ishlatilgan uskuna', 'Xom ashyo', 'Texnolog']
application_category_en_text = ['Equipment', 'Manufacturer', 'Used equipment', 'Raw material', 'Technologist']

application_sub_category_uz_text = ['Sub category 1', 'Sub category 2', 'Sub category 3', 'Sub category 4',
                                    'Sub category 5']
application_sub_category_en_text = ['Sub category 1', 'Sub category 2', 'Sub category 3', 'Sub category 4',
                                    'Sub category 5']

btn_text_admin_panel_uz = ['Kompaniyani tahrirlash', 'E\'lonni tahrirlash', 'kompaniyani o\'chirish',
                           'E\'lonni o\'chirish', 'Axborot byulleteni', 'Admin qo\'shish', 'Rassilka',
                           'Hisob to\'ldirish']
btn_text_admin_panel_en = ['Edit company', 'Edit post', 'Del company', 'Del post', 'Newsletter', 'Add admin',
                           'Mailing list', 'add money']

text_my_cabinet_uz = ['Hamyon', 'Hisobni toldirish']  # 'E\'lonni o\'zgartirish',
text_my_cabinet_en = ['Wallet', 'Top up the account']  # 'Edit announcement',


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
        InlineKeyboardButton(text, callback_data=f"category{text}") for text in
        categories_uz_
    ]
    return markup.add(*result)


def category_en():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f"category{categories_uz_[categories_en_.index(text)]}") for text in
        categories_en_
    ]
    return markup.add(*result)


def sub_category_uz():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f"sub_category{text}")
        for text in sub_categories_uz
    ]
    return markup.add(*result)


def sub_category_en():
    markup = InlineKeyboardMarkup(row_width=2)
    result = [
        InlineKeyboardButton(text, callback_data=f"sub_category{sub_categories_uz[sub_categories_en.index(text)]}") for
        text in
        sub_categories_en
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
    btn = [
        InlineKeyboardButton(name, callback_data=name) for name in result
    ]
    return rkm.add(*btn)


async def get_rating_buttons(company_id):
    worked = 0 if await Company.staff_list(company_id, "w") is None else len(
        [i for i in await Company.staff_list(company_id, 'w')])
    partner = 0 if await Company.staff_list(company_id, "p") is None else len(
        [i for i in await Company.staff_list(company_id, 'p')])
    rating_buttons = [
        InlineKeyboardButton(
            f'👍🏽 {worked}', callback_data=f'w_{company_id}'
        ),
        InlineKeyboardButton(
            f'👎🏽 {partner}', callback_data=f'p_{company_id}'
        )
    ]
    return InlineKeyboardMarkup().add(*rating_buttons)


def application_menu_uz():
    result = [
        InlineKeyboardButton(name, callback_data=application_en[application_uz.index(name)]) for name in application_uz
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def application_menu_en():
    result = [
        InlineKeyboardButton(name, callback_data=name) for name in application_en
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def application_category_uz():
    result = [
        InlineKeyboardButton(category,
                             callback_data=application_category_en_text[application_category_uz_text.index(category)])
        for category in
        application_category_uz_text
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def application_category_en():
    result = [
        InlineKeyboardButton(category, callback_data=category) for category in application_category_en_text
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def application_sub_category_uz():
    result = [
        InlineKeyboardButton(sub_category, callback_data=application_sub_category_en_text.index(sub_category)) for
        sub_category in
        application_sub_category_uz_text
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def application_sub_category_en():
    result = [
        InlineKeyboardButton(sub_category, callback_data=sub_category) for sub_category in
        application_sub_category_en_text
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def admin_panel_uz():
    result = [
        InlineKeyboardButton(name, callback_data=btn_text_admin_panel_en[btn_text_admin_panel_uz.index(name)]) for name
        in btn_text_admin_panel_uz
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def admin_panel_en():
    result = [
        InlineKeyboardButton(name, callback_data=name) for name in btn_text_admin_panel_en
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def my_cabinet_uz():
    result = [
        InlineKeyboardButton(text, callback_data=text_my_cabinet_en[text_my_cabinet_uz.index(text)]) for text in
        text_my_cabinet_uz
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


def my_cabinet_en():
    result = [
        InlineKeyboardButton(text, callback_data=text) for text in
        text_my_cabinet_en
    ]
    return InlineKeyboardMarkup(row_width=2).add(*result)


async def my_announcements(user_id):
    id = await Announcement.get_all(user_id)
    result = [InlineKeyboardButton(f'{i[0].description}', callback_data=i[0].pk) for i in id]
    return InlineKeyboardMarkup().add(*result)
