from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.config import DAILY_CHANNEL_ID
from bot.database import crud
from bot.products import items_from_json, product_name, items_total, unit_label
from sqlalchemy.ext.asyncio import AsyncSession


def _order_items_lines(order):
    """Buyurtma mahsulotlarini kanal xabari uchun formatlaydi."""
    parsed = items_from_json(getattr(order, "items", None))
    if parsed:
        lines = []
        for i in parsed:
            name = product_name(i.get("id", ""), "uz") or i.get("name", "")
            qty = int(i.get("qty", 0))
            price = int(i.get("price", 0))
            unit = unit_label(i.get("unit", "dona"), "uz")
            lines.append(f"💧 {name} × {qty} {unit} = {qty * price:,} so'm")
        return lines
    # Eski buyurtma
    return [f"💧 19 litr × {order.quantity}"]


def format_order_message(order, user, delivered: bool = False):
    status = "✅ YETKAZILDI" if delivered else "⏳ YETKAZILMOQDA"
    total = order.total_price if getattr(order, "total_price", None) is not None else (order.quantity * 15000)
    lines = [
        f"📦 BUYURTMA #{order.order_number:04d}",
        "━" * 30,
        f"👤 Mijoz: {user.full_name}",
        f"📞 Tel: {user.phone}",
        f"🏠 Xonadon: {user.household_size} kishi",
        "─" * 30,
    ]
    lines.extend(_order_items_lines(order))
    lines.append(f"🏁 Jami: {total:,} so'm")
    lines.append(f"📍 Manzil: {order.address}")
    if order.location_lat and order.location_lng:
        lines.append(f"📍 Lokatsiya: {order.location_lat}, {order.location_lng}")
        lines.append(f"🗺 Xarita: https://maps.google.com/maps?q={order.location_lat},{order.location_lng}")
    lines.append(f"📅 Vaqt: {order.created_at.strftime('%d.%m.%Y, %H:%M')}")
    lines.append("━" * 30)
    lines.append(f"🔹 Holat: {status}")
    return "\n".join(lines)


def get_deliver_keyboard(order_id: int, with_courier: bool = True):
    """Kanal buyurtma xabari uchun tugmalar.
    with_courier=True bo'lsa 'Dostavkachiga yuborish' tugmasi ham qo'shiladi (kanal uchun).
    Dostavkachiga yuborilган xabarда faqat 'Yetkazildi' bo'ladi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Yetkazildi", callback_data=f"deliver_{order_id}")
    if with_courier:
        builder.button(text="📤 Dostavkachiga yuborish", callback_data=f"tocourier_{order_id}")
    builder.adjust(1)
    return builder.as_markup()


def get_courier_only_keyboard(order_id: int):
    """Dostavkachiга yuboriladigan xabar uchun — faqat Yetkazildi tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Yetkazildi", callback_data=f"deliver_{order_id}")
    return builder.as_markup()


async def send_order_to_channel(bot: Bot, session: AsyncSession, order, user):
    if not DAILY_CHANNEL_ID:
        return None

    text = format_order_message(order, user)

    if order.location_lat and order.location_lng:
        await bot.send_location(
            chat_id=DAILY_CHANNEL_ID,
            latitude=order.location_lat,
            longitude=order.location_lng
        )

    message = await bot.send_message(
        chat_id=DAILY_CHANNEL_ID,
        text=text,
        reply_markup=get_deliver_keyboard(order.id)
    )
    await crud.update_order_channel_message_id(session, order.id, message.message_id)
    return message
