from sqlalchemy import select, update, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User, Order, Admin, OrderStatus, get_uzbekistan_time
from datetime import datetime, date, timedelta


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, telegram_id: int, full_name: str, phone: str, household_size: int, language: str = "uz"):
    user = User(
        telegram_id=telegram_id,
        full_name=full_name,
        phone=phone,
        household_size=household_size,
        language=language
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_language(session: AsyncSession, user_id: int, language: str):
    await session.execute(update(User).where(User.id == user_id).values(language=language))
    await session.commit()


async def update_user_name(session: AsyncSession, user_id: int, new_name: str):
    await session.execute(update(User).where(User.id == user_id).values(full_name=new_name))
    await session.commit()


async def update_user_phone(session: AsyncSession, user_id: int, new_phone: str):
    await session.execute(update(User).where(User.id == user_id).values(phone=new_phone))
    await session.commit()


async def update_user_household(session: AsyncSession, user_id: int, household_size: int):
    await session.execute(
        update(User).where(User.id == user_id).values(household_size=household_size)
    )
    await session.commit()


async def update_user_location(session: AsyncSession, user_id: int, address: str,
                               lat: float = None, lng: float = None):
    """Foydalanuvchining saqlangan manzil/lokatsiyasini yangilaydi."""
    await session.execute(
        update(User).where(User.id == user_id).values(
            saved_address=address, saved_lat=lat, saved_lng=lng
        )
    )
    await session.commit()


async def update_user_reminder_at(session: AsyncSession, user_id: int):
    await session.execute(
        update(User).where(User.id == user_id).values(last_reminder_at=get_uzbekistan_time())
    )
    await session.commit()


async def get_last_order_number(session: AsyncSession):
    result = await session.execute(select(func.max(Order.order_number)))
    return result.scalar() or 0


async def create_order(session: AsyncSession, user_id: int, order_number: int,
                       quantity: int, address: str, location_lat: float = None,
                       location_lng: float = None, items: str = None, total_price: int = None):
    order = Order(
        user_id=user_id,
        order_number=order_number,
        quantity=quantity,
        items=items,
        total_price=total_price,
        address=address,
        location_lat=location_lat,
        location_lng=location_lng,
        status=OrderStatus.pending
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def get_orders_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    )
    return result.scalars().all()


async def get_active_orders_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Order).where(and_(Order.user_id == user_id, Order.status == OrderStatus.pending))
    )
    return result.scalars().all()


async def get_order_by_id(session: AsyncSession, order_id: int):
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def update_order_channel_message_id(session: AsyncSession, order_id: int, message_id: int):
    await session.execute(update(Order).where(Order.id == order_id).values(channel_message_id=message_id))
    await session.commit()


async def mark_order_delivered(session: AsyncSession, order_id: int):
    await session.execute(
        update(Order).where(Order.id == order_id).values(status=OrderStatus.delivered)
    )
    await session.commit()


async def get_admin_by_telegram_id(session: AsyncSession, telegram_id: int):
    result = await session.execute(select(Admin).where(Admin.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create_admin(session: AsyncSession, telegram_id: int, full_name: str):
    admin = Admin(telegram_id=telegram_id, full_name=full_name)
    session.add(admin)
    await session.commit()
    return admin


async def get_orders_count_by_date_range(session: AsyncSession, start_date: date, end_date: date):
    result = await session.execute(
        select(func.count(Order.id)).where(
            and_(func.date(Order.created_at) >= start_date, func.date(Order.created_at) <= end_date)
        )
    )
    return result.scalar() or 0


async def get_orders_by_date_range(session: AsyncSession, start_date: date, end_date: date):
    result = await session.execute(
        select(Order).where(
            and_(func.date(Order.created_at) >= start_date, func.date(Order.created_at) <= end_date)
        ).order_by(Order.created_at.asc())
    )
    return result.scalars().all()


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User).order_by(User.id))
    return result.scalars().all()
