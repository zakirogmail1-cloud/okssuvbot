"""
Sticker yuborish uchun yordamchi klass.
Sticker file_id larini .env faylida yoki ushbu faylda sozlash mumkin.

Sticker qo'shish:
1. @Stickers bot ga yozib, o'zingizga yoqqan stiker yarating
2. Botga stikerni yuboring
3. Telegram Web'dan stiker file_id sini oling
4. Quyidagi o'zgaruvchilarga yozib qo'ying
"""

import logging

logger = logging.getLogger(__name__)

# STICKER FILE ID LARINI SHU YERGA YOZING
# @Stickers bot orqali yarating va file_id ni oling
# Misol:
# WELCOME_STICKER = "CAACAgIAAxkB..."
# ORDER_STICKER = "CAACAgIAAxkB..."
# SUCCESS_STICKER = "CAACAgIAAxkB..."

WELCOME_STICKER = None
ORDER_STICKER = None
SUCCESS_STICKER = None


class Stickers:
    """Sticker yuborish uchun yordamchi klass.
    Agar sticker file_id sozlanmagan bo'lsa, stiker yuborilmaydi.
    """

    @staticmethod
    async def _send(bot, chat_id: int, sticker_id: str | None):
        if not sticker_id:
            return
        try:
            await bot.send_sticker(chat_id=chat_id, sticker=sticker_id)
        except Exception as e:
            logger.warning(f"Sticker yuborishda xatolik: {e}")

    @staticmethod
    async def welcome(bot, chat_id: int):
        await Stickers._send(bot, chat_id, WELCOME_STICKER)

    @staticmethod
    async def order(bot, chat_id: int):
        await Stickers._send(bot, chat_id, ORDER_STICKER)

    @staticmethod
    async def success(bot, chat_id: int):
        await Stickers._send(bot, chat_id, SUCCESS_STICKER)
