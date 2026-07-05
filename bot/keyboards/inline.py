from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.localization import get_text


def get_language_inline_keyboard():
    """Til tanlash inline klaviaturasi"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbek", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.adjust(1)
    return builder.as_markup()


def get_order_confirm_keyboard(lang: str = "uz"):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_confirm", lang), callback_data="confirm_order")
    builder.button(text=get_text("btn_cancel", lang), callback_data="cancel_order")
    return builder.as_markup()


def get_order_cancel_keyboard(order_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Bekor qilish", callback_data=f"cancel_order_{order_id}")
    return builder.as_markup()
