from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.localization import get_text
from bot.products import (
    PRODUCTS, product_name, items_count, items_total, build_items, unit_label,
)


def get_products_cart_keyboard(cart: dict, lang: str = "uz") -> InlineKeyboardMarkup:
    """Har bir mahsulot uchun ➖ [son] ➕ selektorli savat klaviaturasi."""
    rows = []
    for p in PRODUCTS:
        pid = p["id"]
        qty = int(cart.get(pid, 0))
        name = product_name(pid, lang)
        unit = unit_label(p.get("unit", "dona"), lang)
        mn = p.get("min_qty", 1)
        # 1-qator: mahsulot nomi, narxi va minimal buyurtma
        rows.append([
            InlineKeyboardButton(
                text=f"{p['emoji']} {name} — {p['price']:,} so'm  (min {mn} {unit})",
                callback_data="noop"
            )
        ])
        # 2-qator: ➖ [son birlik] ➕
        rows.append([
            InlineKeyboardButton(text="➖", callback_data=f"qdec_{pid}"),
            InlineKeyboardButton(text=f"{qty} {unit}", callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data=f"qinc_{pid}"),
        ])

    # Savat xulosasi
    items = build_items(cart)
    rows.append([
        InlineKeyboardButton(
            text=get_text("cart_summary", lang, count=items_count(items), total=f"{items_total(items):,}"),
            callback_data="noop"
        )
    ])
    # Davom etish / bekor qilish
    rows.append([InlineKeyboardButton(text=get_text("btn_continue", lang), callback_data="order_next")])
    rows.append([InlineKeyboardButton(text=get_text("btn_cancel", lang), callback_data="cancel_order")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


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
