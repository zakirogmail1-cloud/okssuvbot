import os
from dotenv import load_dotenv
from datetime import timezone, timedelta

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

_daily_channel = os.getenv("DAILY_CHANNEL_ID", "")
if not _daily_channel or _daily_channel == "0":
    DAILY_CHANNEL_ID = None
else:
    DAILY_CHANNEL_ID = int(_daily_channel)

ADMIN_TELEGRAM_IDS = [int(x) for x in os.getenv("ADMIN_TELEGRAM_IDS", "").split(",") if x]

UZBEKISTAN_TZ = timezone(timedelta(hours=5))


def get_current_time():
    from datetime import datetime
    return datetime.now(UZBEKISTAN_TZ).replace(tzinfo=None)


def get_current_date():
    return get_current_time().date()
