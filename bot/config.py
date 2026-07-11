import os
import logging
from dotenv import load_dotenv
from datetime import timezone, timedelta

load_dotenv()

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not BOT_TOKEN:
    logger.warning("BOT_TOKEN is not set in environment variables")
if not DATABASE_URL:
    logger.warning("DATABASE_URL is not set in environment variables")

_daily_channel = os.getenv("DAILY_CHANNEL_ID", "")
if not _daily_channel or _daily_channel == "0":
    DAILY_CHANNEL_ID = None
else:
    DAILY_CHANNEL_ID = int(_daily_channel)

def _parse_admin_ids(raw: str) -> list[int]:
    ids: list[int] = []
    for entry in raw.split(","):
        trimmed = entry.strip()
        if not trimmed:
            continue
        try:
            ids.append(int(trimmed))
        except ValueError:
            logger.warning("Ignoring invalid ADMIN_TELEGRAM_IDS entry: %r", entry)
    return ids


ADMIN_TELEGRAM_IDS = _parse_admin_ids(os.getenv("ADMIN_TELEGRAM_IDS", ""))

# Dostavkachilar (yetkazib beruvchilar).
# Format: DELIVERY_STAFF=123456789:Ali,987654321:Vali
# (ism ixtiyoriy; ":ism" bo'lmasa avtomatik nom beriladi)
DELIVERY_STAFF = []
for _part in os.getenv("DELIVERY_STAFF", "").split(","):
    _part = _part.strip()
    if not _part:
        continue
    if ":" in _part:
        _id, _name = _part.split(":", 1)
        try:
            DELIVERY_STAFF.append((int(_id.strip()), _name.strip() or f"Dostavkachi {_id.strip()}"))
        except ValueError:
            pass
    else:
        try:
            DELIVERY_STAFF.append((int(_part), f"Dostavkachi {_part}"))
        except ValueError:
            pass

UZBEKISTAN_TZ = timezone(timedelta(hours=5))


def get_current_time():
    from datetime import datetime
    return datetime.now(UZBEKISTAN_TZ).replace(tzinfo=None)


def get_current_date():
    return get_current_time().date()
