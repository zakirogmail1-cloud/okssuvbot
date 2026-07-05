from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.config import DAILY_CHANNEL_ID
from bot.database import crud
from sqlalchemy.ext.asyncio import AsyncSession


def format_order_message(order, user, delivered: bool = False):
    status = "✅ YETKAZILDI" if delivered else "⏳ YETKAZILMOQDA"
    lines = [
        f"📦 BUYURTMA #{order.order_number:04d}",
        "━" * 30,
        f"👤 Mijoz: {user.full_name}",
        f"📞 Tel: {user.phone}",
        f"🏠 Xonadon: {user.household_size} kishi",
        "─" * 30,
        f"💧 19 litr × {order.quantity}",
        f"📍 Manzil: {order.address}",
    ]
    if order.location_lat and order.location_lng:
        lines.append(f"📍 Lokatsiya: {order.location_lat}, {order.location_lng}")
        lines.append(f"🗺 Xarita: https://maps.google.com/maps?q={order.location_lat},{order.location_lng}")
    lines.append(f"📅 Vaqt: {order.created_at.strftime('%d.%m.%Y, %H:%M')}")
    lines.append("━" * 30)
    lines.append(f"🔹 Holat: {status}")
    return "\n".join(lines)


def get_deliver_keyboard(order_id: int):
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
