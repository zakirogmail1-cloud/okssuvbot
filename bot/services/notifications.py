from aiogram import Bot
from bot.database.connection import async_session
from bot.database import crud
from bot.config import get_current_time
import logging

logger = logging.getLogger(__name__)

REMINDER_INTERVALS = {
    4: 7,
    5: 5,
    6: 4,
    7: 3,
}

DEFAULT_INTERVAL_DAYS = 5

REMINDER_MESSAGE = (
    "\U0001f4a7 <b>Diqqat! Suvingiz oxirlab qoldi!</b>\n\n"
    "Assalomu alaykum, {full_name}!\n"
    "Toza va sifatli ichimlik suvi — sog'lik garovi.\n"
    "Yana suv buyurtma berish vaqti keldi!\n\n"
    "\U0001f6ce\u00a0<b>Buyurtma berish</b> tugmasini bosing va "
    "biz sizga eng yaqin vaqtda yetkazib beramiz.\n\n"
    "\U0001f64f Rahmat!\n"
    "<i>OKS Suv — toza suv, sog' hayot!</i> \U0001f4a7"
)


def get_reminder_interval(household_size: int) -> int:
    return REMINDER_INTERVALS.get(household_size, DEFAULT_INTERVAL_DAYS)


async def send_water_reminders(bot: Bot):
    logger.info("Checking water reminders for all users...")

    async with async_session() as session:
        users = await crud.get_all_users(session)
        now = get_current_time()

        for user in users:
            try:
                interval_days = get_reminder_interval(user.household_size)
                orders = await crud.get_orders_by_user(session, user.id)

                if orders:
                    last_order = orders[0]
                    if last_order.status.name != "delivered":
                        continue
                    days_since = (now - last_order.created_at).days
                else:
                    days_since = (now - user.created_at).days

                if days_since < interval_days:
                    continue

                if user.last_reminder_at:
                    days_since_last_reminder = (now - user.last_reminder_at).days
                    if days_since_last_reminder < interval_days:
                        continue

                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=REMINDER_MESSAGE.format(full_name=user.full_name)
                )

                await crud.update_user_reminder_at(session, user.id)
                logger.info(f"Reminder sent to {user.full_name} (tg:{user.telegram_id})")

            except Exception as e:
                logger.warning(f"Failed to send reminder to user {user.telegram_id}: {e}")
                continue

    logger.info("Water reminders check completed.")
