import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent
from bot.config import BOT_TOKEN, ADMIN_TELEGRAM_IDS
from bot.database.connection import init_db, async_session
from bot.database import crud
from bot.handlers import start, orders, admin
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.services.scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def seed_admins():
    async with async_session() as session:
        for tid in ADMIN_TELEGRAM_IDS:
            existing = await crud.get_admin_by_telegram_id(session, tid)
            if not existing:
                await crud.create_admin(session, telegram_id=tid, full_name=f"Admin_{tid}")


async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set in .env")
        return

    logger.info("Connecting to database...")

    await init_db()
    logger.info("Database initialized")

    await seed_admins()
    logger.info("Admins seeded")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    @dp.errors()
    async def error_handler(event: ErrorEvent):
        logger.error(f"Handler error: {event.exception}", exc_info=True)

    dp.include_router(start.router)
    dp.include_router(orders.router)
    dp.include_router(admin.router)

    dp.message.middleware(ThrottlingMiddleware())

    webhook_info = await bot.get_webhook_info()
    logger.info(f"Current webhook: {webhook_info.url}")

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleared, starting polling...")

    bot_info = await bot.get_me()
    logger.info(f"Bot: @{bot_info.username} (ID: {bot_info.id})")

    scheduler = setup_scheduler(bot)
    logger.info("Scheduler started")

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
