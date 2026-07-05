from aiogram import BaseMiddleware
from aiogram.types import Message
from collections import defaultdict
from typing import Dict, List
import time


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = 30, per_seconds: int = 60):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.user_messages: Dict[int, List[float]] = defaultdict(list)

    async def __call__(self, handler, event: Message, data: dict):
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.time()
        self.user_messages[user_id] = [t for t in self.user_messages[user_id] if now - t < self.per_seconds]

        if len(self.user_messages[user_id]) >= self.rate_limit:
            await event.answer("⏳ Biroz kuting, juda ko'p so'rov yubordingiz.")
            return

        self.user_messages[user_id].append(now)
        return await handler(event, data)
