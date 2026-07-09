from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot.localization import get_text


def get_language_keyboard():
    """Til tanlash klaviaturasi"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbek")],
            [KeyboardButton(text="🇷🇺 Русский")],
            [KeyboardButton(text="🇬🇧 English")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_contact_keyboard(lang: str = "uz"):
    button = KeyboardButton(text=get_text("btn_send_phone", lang), request_contact=True)
    return ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_main_keyboard(lang: str = "uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            # Birinchi qator - 2 ta tugma
            [
                KeyboardButton(text=get_text("btn_order", lang)),
                KeyboardButton(text=get_text("btn_my_orders", lang))
            ],
            # Ikkinchi qator - 2 ta tugma
            [
                KeyboardButton(text=get_text("btn_my_info", lang)),
                KeyboardButton(text=get_text("btn_about_us", lang))
            ],
            # Uchinchi qator - 2 ta tugma
            [
                KeyboardButton(text=get_text("btn_support", lang)),
                KeyboardButton(text=get_text("btn_change_language", lang))
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Menyudan birini tanlang..."
    )


def get_product_keyboard(lang: str = "uz"):
    from bot.localization import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("product_19l", lang))],
            [KeyboardButton(text=get_text("btn_back", lang))],
        ],
        resize_keyboard=True
    )


def get_location_keyboard(lang: str = "uz"):
    from bot.localization import get_text
    button = KeyboardButton(text=get_text("btn_send_location", lang), request_location=True)
    return ReplyKeyboardMarkup(
        keyboard=[[button], [KeyboardButton(text=get_text("btn_back", lang))]],
        resize_keyboard=True
    )


def get_admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Kunlik hisobot")],
            [KeyboardButton(text="📊 Haftalik hisobot")],
            [KeyboardButton(text="📊 Oylik hisobot")],
            [KeyboardButton(text="👥 Barcha mijozlar (Excel)")],
            [KeyboardButton(text="📢 Xabar yuborish")],
            [KeyboardButton(text="◀️ Chiqish")],
        ],
        resize_keyboard=True
    )


def get_info_edit_keyboard(lang: str = "uz"):
    from bot.localization import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("btn_edit_name", lang))],
            [KeyboardButton(text=get_text("btn_edit_phone", lang))],
            [KeyboardButton(text=get_text("btn_edit_household", lang))],
            [KeyboardButton(text=get_text("btn_edit_address", lang))],
            [KeyboardButton(text=get_text("btn_back", lang))],
        ],
        resize_keyboard=True
    )


def get_edit_location_keyboard(lang: str = "uz"):
    from bot.localization import get_text
    button = KeyboardButton(text=get_text("btn_send_location", lang), request_location=True)
    return ReplyKeyboardMarkup(
        keyboard=[[button], [KeyboardButton(text=get_text("btn_back", lang))]],
        resize_keyboard=True
    )
