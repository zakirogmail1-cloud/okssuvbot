#!/usr/bin/env python3
"""Timezone test script - O'zbekiston vaqti test qilish uchun"""

from datetime import datetime
from bot.config import get_current_time, get_current_date, UZBEKISTAN_TZ

print("=" * 50)
print("TIMEZONE TEST - O'ZBEKISTON VAQTI")
print("=" * 50)

# UTC vaqti
utc_now = datetime.utcnow()
print(f"\n📅 UTC vaqti: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")

# O'zbekiston vaqti
uz_now = get_current_time()
print(f"📅 O'zbekiston vaqti: {uz_now.strftime('%Y-%m-%d %H:%M:%S')}")

# Sana
today = get_current_date()
print(f"📅 Bugungi sana: {today.strftime('%d.%m.%Y')}")

print(f"\n✅ Farq: +5 soat (O'zbekiston UTC+5)")
print(f"✅ Timezone: {UZBEKISTAN_TZ}")
print("=" * 50)
