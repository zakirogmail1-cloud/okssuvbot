from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.services.notifications import send_water_reminders
import logging

logger = logging.getLogger(__name__)


def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_water_reminders,
        CronTrigger(hour=10, minute=0),
        args=[bot],
        id="water_reminder_daily",
        replace_existing=True,
        name="Kunlik suv eslatmasi"
    )

    logger.info("Daily water reminder job scheduled at 10:00")
    scheduler.start()
    return scheduler
