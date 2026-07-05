import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from bot.database.connection import async_session
from bot.database import crud
from bot.database.models import OrderStatus, User
from bot.keyboards.inline import get_order_confirm_keyboard
from bot.services.channel import send_order_to_channel, format_order_message
from bot.config import DAILY_CHANNEL_ID
from bot.utils.stickers import Stickers
from bot.keyboards.reply import get_main_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.localization import get_text

logger = logging.getLogger(__name__)
router = Router()


class OrderState(StatesGroup):
    choosing_product = State()
    entering_quantity = State()
    waiting_location = State()
    entering_address = State()
    confirming_order = State()


def get_location_keyboard(lang: str = "uz"):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text("btn_send_location", lang), request_location=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )


def product_kb(lang: str = "uz"):
    b = InlineKeyboardBuilder()
    b.button(text=get_text("product_19l", lang), callback_data="product_19L")
    b.button(text=get_text("product_cancel", lang), callback_data="cancel_order")
    return b.as_markup()


def back_kb(lang: str = "uz"):
    b = InlineKeyboardBuilder()
    b.button(text=get_text("btn_back", lang), callback_data="back_to_products")
    return b.as_markup()


async def edit_main(state: FSMContext, bot: Bot, text: str, reply_markup=None):
    data = await state.get_data()
    try:
        await bot.edit_message_text(
            text=text,
            chat_id=data["main_chat_id"],
            message_id=data["main_msg_id"],
            reply_markup=reply_markup
        )
        return True
    except Exception as e:
        logger.warning(f"edit_main: {e}")
        return False


async def del_later(bot: Bot, chat_id: int, msg_id: int, delay: int = 3):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except Exception:
        pass


async def del_temp(state: FSMContext, bot: Bot):
    d = await state.get_data()
    tid = d.get("temp_msg_id")
    tch = d.get("temp_chat_id")
    if tid and tch:
        try:
            await bot.delete_message(chat_id=tch, message_id=tid)
        except Exception:
            pass
        await state.update_data(temp_msg_id=None, temp_chat_id=None)


# ─── BUYURTMA BOSHLASH ───

@router.message(F.text.in_(["🛒 Buyurtma berish", "🛒 Заказать", "🛒 Place Order"]))
async def start_order(message: Message, state: FSMContext):
    try:
        async with async_session() as s:
            user = await crud.get_user_by_telegram_id(s, message.from_user.id)
        if not user:
            await message.answer(get_text("please_register", "uz"))
            return

        lang = user.language
        async with async_session() as s:
            active = await crud.get_active_orders_by_user(s, user.id)
            if active:
                await message.answer(
                    get_text("order_active_warning", lang),
                    reply_markup=get_main_keyboard(lang)
                )
                return

        await Stickers.order(message.bot, message.chat.id)

        msg = await message.answer(
            get_text("order_start", lang),
            reply_markup=product_kb(lang)
        )
        await state.update_data(main_msg_id=msg.message_id, main_chat_id=msg.chat.id, user_lang=lang)
        await state.set_state(OrderState.choosing_product)
    except Exception as e:
        logger.error(f"start_order: {e}", exc_info=True)


# ─── MAHSULOT TANLASH ───

@router.callback_query(OrderState.choosing_product, F.data == "product_19L")
async def choose_product(callback: CallbackQuery, state: FSMContext):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        
        await state.update_data(product="19L_15K")
        await state.set_state(OrderState.entering_quantity)

        await edit_main(state, callback.bot,
            get_text("order_quantity", lang),
            reply_markup=back_kb(lang)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"choose_product: {e}", exc_info=True)
        await callback.answer("Xatolik", show_alert=True)


@router.callback_query(OrderState.choosing_product, F.data == "cancel_order")
async def cancel_from_start(callback: CallbackQuery, state: FSMContext):
    d = await state.get_data()
    lang = d.get("user_lang", "uz")
    
    await state.clear()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    
    # Asosiy klaviaturani qaytarish
    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text=get_text("order_cancelled", lang),
        reply_markup=get_main_keyboard(lang)
    )
    await callback.answer()


# ─── SON KIRITISH ───

@router.message(OrderState.entering_quantity, F.text.func(lambda t: t.strip().isdigit() and int(t.strip()) > 0))
async def enter_quantity(message: Message, state: FSMContext):
    try:
        q = int(message.text.strip())
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        
        await state.update_data(quantity=q)
        await state.set_state(OrderState.waiting_location)
        try:
            await message.delete()
        except Exception:
            pass

        await edit_main(state, message.bot,
            get_text("order_location", lang)
        )

        temp = await message.answer(
            get_text("order_location_prompt", lang),
            reply_markup=get_location_keyboard(lang)
        )
        await state.update_data(temp_msg_id=temp.message_id, temp_chat_id=temp.chat.id)
    except Exception as e:
        logger.error(f"enter_quantity: {e}", exc_info=True)


@router.message(OrderState.entering_quantity)
async def q_invalid(message: Message, state: FSMContext):
    d = await state.get_data()
    lang = d.get("user_lang", "uz")
    
    try:
        await message.delete()
    except Exception:
        pass
    m = await message.answer(get_text("invalid_quantity", lang))
    asyncio.ensure_future(del_later(message.bot, m.chat.id, m.message_id, 3))


# ─── LOKATSIYA / MANZIL ───

@router.message(OrderState.waiting_location, F.location)
async def process_location(message: Message, state: FSMContext):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        
        await state.update_data(location_lat=message.location.latitude, location_lng=message.location.longitude)
        await del_temp(state, message.bot)
        await state.set_state(OrderState.entering_address)
        try:
            await message.delete()
        except Exception:
            pass
        await edit_main(state, message.bot,
            get_text("order_address", lang)
        )
    except Exception as e:
        logger.error(f"process_location: {e}", exc_info=True)


@router.message(OrderState.waiting_location, F.text.func(lambda t: len(t.strip()) >= 5))
async def addr_direct(message: Message, state: FSMContext):
    try:
        await del_temp(state, message.bot)
        await state.update_data(address=message.text.strip())
        try:
            await message.delete()
        except Exception:
            pass
        await show_confirm(message, state)
    except Exception as e:
        logger.error(f"addr_direct: {e}", exc_info=True)


@router.message(OrderState.waiting_location)
async def loc_invalid(message: Message, state: FSMContext):
    d = await state.get_data()
    lang = d.get("user_lang", "uz")
    
    try:
        await message.delete()
    except Exception:
        pass
    m = await message.answer(get_text("invalid_location", lang))
    asyncio.ensure_future(del_later(message.bot, m.chat.id, m.message_id, 3))


# ─── MANZIL KIRITISH ───

@router.message(OrderState.entering_address, F.text.func(lambda t: len(t.strip()) >= 5))
async def enter_address(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text.strip())
        try:
            await message.delete()
        except Exception:
            pass
        await show_confirm(message, state)
    except Exception as e:
        logger.error(f"enter_address: {e}", exc_info=True)


@router.message(OrderState.entering_address)
async def addr_invalid(message: Message, state: FSMContext):
    d = await state.get_data()
    lang = d.get("user_lang", "uz")
    
    try:
        await message.delete()
    except Exception:
        pass
    m = await message.answer(get_text("invalid_address", lang))
    asyncio.ensure_future(del_later(message.bot, m.chat.id, m.message_id, 3))


# ─── TASDIQLASH ───

async def show_confirm(msg: Message, state: FSMContext):
    d = await state.get_data()
    lang = d.get("user_lang", "uz")
    total = d["quantity"] * 15000
    addr = d.get("address", "")
    await state.set_state(OrderState.confirming_order)
    await edit_main(state, msg.bot,
        get_text("order_confirm", lang, quantity=d['quantity'], total=f"{total:,}", address=addr),
        reply_markup=get_order_confirm_keyboard()
    )


@router.callback_query(OrderState.confirming_order, F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        
        async with async_session() as s:
            user = await crud.get_user_by_telegram_id(s, callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                await state.clear()
                return

            last = await crud.get_last_order_number(s)
            num = last + 1
            order = await crud.create_order(s, user_id=user.id, order_number=num,
                quantity=d["quantity"], address=d.get("address", ""),
                location_lat=d.get("location_lat"), location_lng=d.get("location_lng"))

            if DAILY_CHANNEL_ID:
                await send_order_to_channel(callback.bot, s, order, user)

        await edit_main(state, callback.bot,
            get_text("order_success", lang, number=f"{num:04d}", quantity=d['quantity'], address=d.get('address', ''))
        )

        await Stickers.success(callback.bot, callback.from_user.id)
        
        # Asosiy klaviaturani qaytarish
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=get_text("main_menu", lang),
            reply_markup=get_main_keyboard(lang)
        )
        
        await state.clear()
        await callback.answer()
    except Exception as e:
        logger.error(f"confirm_order: {e}", exc_info=True)
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        await state.clear()
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=get_text("order_error", lang),
            reply_markup=get_main_keyboard(lang)
        )
        await callback.answer("Xatolik", show_alert=True)


@router.callback_query(F.data == "cancel_order")
async def cancel_anywhere(callback: CallbackQuery, state: FSMContext):
    d = await state.get_data()
    lang = d.get("user_lang", "uz")
    
    await state.clear()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    
    # Asosiy klaviaturani qaytarish
    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text=get_text("order_cancelled", lang),
        reply_markup=get_main_keyboard(lang)
    )
    await callback.answer()


# ─── KANALDAN YETKAZILDI ───

@router.callback_query(F.data.startswith("deliver_"))
async def deliver_order(callback: CallbackQuery):
    try:
        oid = int(callback.data.split("_")[1])
        async with async_session() as s:
            order = await crud.get_order_by_id(s, oid)
            if not order:
                await callback.answer("Buyurtma topilmadi", show_alert=True)
                return
            if order.status == OrderStatus.delivered:
                await callback.answer("Buyurtma allaqachon yetkazilgan", show_alert=True)
                return
            r = await s.execute(select(User).where(User.id == order.user_id))
            customer = r.scalar_one_or_none()
            await crud.mark_order_delivered(s, order.id)

        t = format_order_message(order, customer, delivered=True)
        try:
            await callback.message.edit_text(text=t, reply_markup=None)
        except Exception:
            pass
        await callback.answer("✅ Buyurtma yetkazildi deb belgilandi!", show_alert=True)
    except Exception as e:
        logger.error(f"deliver_order: {e}", exc_info=True)
        await callback.answer("Xatolik", show_alert=True)


# ─── ORQAGA ───

@router.callback_query(F.data == "back_to_products")
async def back_to_products(callback: CallbackQuery, state: FSMContext):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        
        await state.set_state(OrderState.choosing_product)
        ok = await edit_main(state, callback.bot,
            get_text("order_start", lang),
            reply_markup=product_kb(lang)
        )
        if not ok:
            await state.clear()
            await callback.answer("Xatolik", show_alert=True)
            return
        await callback.answer()
    except Exception as e:
        logger.error(f"back_to_products: {e}", exc_info=True)
        await callback.answer("Xatolik", show_alert=True)
        await state.clear()


# ─── MENING BUYURTMALARIM ───

@router.message(F.text.in_(["📋 Mening buyurtmalarim", "📋 Мои заказы", "📋 My Orders"]))
async def my_orders(message: Message):
    try:
        async with async_session() as s:
            user = await crud.get_user_by_telegram_id(s, message.from_user.id)
        if not user:
            await message.answer(get_text("please_register", "uz"))
            return

        lang = user.language
        async with async_session() as s:
            orders = await crud.get_orders_by_user(s, user.id)

        if not orders:
            await message.answer(
                get_text("my_orders_empty", lang),
                reply_markup=get_main_keyboard(lang)
            )
            return

        await message.answer(get_text("my_orders_title", lang))
        for o in orders[:10]:
            st = get_text("order_status_delivered", lang) if o.status == OrderStatus.delivered else get_text("order_status_pending", lang)
            si = "✅" if o.status == OrderStatus.delivered else "⏳"
            await message.answer(
                f"{si} <b>Buyurtma #{o.order_number:04d}</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"💧 19 litr × {o.quantity} = {o.quantity * 15000:,} so'm\n"
                f"📍 {o.address}\n"
                f"📅 {o.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"🔹 {st}"
            )
    except Exception as e:
        logger.error(f"my_orders: {e}", exc_info=True)
