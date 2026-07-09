import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from bot.database.connection import get_db
from bot.database import crud
from bot.database.models import OrderStatus, User
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.keyboards.inline import get_order_confirm_keyboard, get_products_cart_keyboard
from bot.services.channel import (
    send_order_to_channel, format_order_message,
    get_deliver_keyboard, get_courier_only_keyboard,
)
from bot.config import DAILY_CHANNEL_ID, DELIVERY_STAFF
from bot.utils.stickers import Stickers
from bot.keyboards.reply import get_main_keyboard
from bot.localization import get_text
from bot.products import (
    PRODUCTS, get_product, build_items, items_to_json, items_total,
    items_count, format_items_lines, step_qty,
)

logger = logging.getLogger(__name__)
router = Router()

MAX_QTY = 99


class OrderState(StatesGroup):
    selecting = State()          # mahsulot va sonini tanlash
    waiting_location = State()   # lokatsiya so'rash (faqat birinchi marta)
    entering_address = State()   # aniq manzil matni
    confirming_order = State()   # tasdiqlash


def get_location_keyboard(lang: str = "uz"):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text("btn_send_location", lang), request_location=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )


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
        async with get_db() as s:
            user = await crud.get_user_by_telegram_id(s, message.from_user.id)
        if not user:
            await message.answer(get_text("please_register", "uz"))
            return

        lang = user.language

        async with get_db() as s:
            active = await crud.get_active_orders_by_user(s, user.id)
            if active:
                await message.answer(
                    get_text("order_active_warning", lang),
                    reply_markup=get_main_keyboard(lang)
                )
                return

        await Stickers.order(message.bot, message.chat.id)

        cart = {p["id"]: 0 for p in PRODUCTS}
        msg = await message.answer(
            get_text("order_choose_products", lang),
            reply_markup=get_products_cart_keyboard(cart, lang)
        )
        await state.update_data(
            main_msg_id=msg.message_id, main_chat_id=msg.chat.id,
            user_lang=lang, cart=cart
        )
        await state.set_state(OrderState.selecting)
    except Exception as e:
        logger.error(f"start_order: {e}", exc_info=True)


# ─── SON TANLASH (➕ / ➖) ───

@router.callback_query(OrderState.selecting, F.data.startswith("qinc_"))
async def qty_inc(callback: CallbackQuery, state: FSMContext):
    await _change_qty(callback, state, +1)


@router.callback_query(OrderState.selecting, F.data.startswith("qdec_"))
async def qty_dec(callback: CallbackQuery, state: FSMContext):
    await _change_qty(callback, state, -1)


async def _change_qty(callback: CallbackQuery, state: FSMContext, delta: int):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        cart = dict(d.get("cart", {}))
        pid = callback.data.split("_", 1)[1]

        if not get_product(pid):
            await callback.answer()
            return

        cur = int(cart.get(pid, 0))
        new = step_qty(pid, cur, delta)
        cart[pid] = new
        await state.update_data(cart=cart)

        if new != cur:
            try:
                await callback.message.edit_reply_markup(
                    reply_markup=get_products_cart_keyboard(cart, lang)
                )
            except Exception as e:
                logger.warning(f"_change_qty edit: {e}")
        await callback.answer()
    except Exception as e:
        logger.error(f"_change_qty: {e}", exc_info=True)
        await callback.answer()


@router.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery):
    await callback.answer()


# ─── DAVOM ETISH ───

@router.callback_query(OrderState.selecting, F.data == "order_next")
async def order_next(callback: CallbackQuery, state: FSMContext):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        cart = d.get("cart", {})
        items = build_items(cart)

        if not items:
            await callback.answer(get_text("cart_empty", lang), show_alert=True)
            return

        await state.update_data(items=items, total=items_total(items))

        # Saqlangan manzil bormi?
        async with get_db() as s:
            user = await crud.get_user_by_telegram_id(s, callback.from_user.id)

        if user and user.saved_address:
            # Lokatsiya so'ramaymiz — saqlanganini ishlatamiz
            await state.update_data(
                address=user.saved_address,
                location_lat=user.saved_lat,
                location_lng=user.saved_lng
            )
            await callback.answer()
            await show_confirm(callback.message, state)
            return

        # Birinchi marta — lokatsiya so'raymiz
        await state.set_state(OrderState.waiting_location)
        await edit_main(state, callback.bot, get_text("order_location", lang))
        temp = await callback.message.answer(
            get_text("order_location_prompt", lang),
            reply_markup=get_location_keyboard(lang)
        )
        await state.update_data(temp_msg_id=temp.message_id, temp_chat_id=temp.chat.id)
        await callback.answer()
    except Exception as e:
        logger.error(f"order_next: {e}", exc_info=True)
        await callback.answer("Xatolik", show_alert=True)


# ─── LOKATSIYA / MANZIL ───

@router.message(OrderState.waiting_location, F.location)
async def process_location(message: Message, state: FSMContext):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        await state.update_data(
            location_lat=message.location.latitude,
            location_lng=message.location.longitude
        )
        await del_temp(state, message.bot)
        await state.set_state(OrderState.entering_address)
        try:
            await message.delete()
        except Exception:
            pass
        await edit_main(state, message.bot, get_text("order_address", lang))
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
        await _save_location_to_profile(message, state)
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


@router.message(OrderState.entering_address, F.text.func(lambda t: len(t.strip()) >= 5))
async def enter_address(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text.strip())
        try:
            await message.delete()
        except Exception:
            pass
        await _save_location_to_profile(message, state)
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


async def _save_location_to_profile(message: Message, state: FSMContext):
    """Birinchi buyurtmadagi manzilni foydalanuvchi profiliga saqlaydi."""
    try:
        d = await state.get_data()
        async with get_db() as s:
            user = await crud.get_user_by_telegram_id(s, message.from_user.id)
            if user:
                await crud.update_user_location(
                    s, user.id,
                    address=d.get("address", ""),
                    lat=d.get("location_lat"),
                    lng=d.get("location_lng")
                )
    except Exception as e:
        logger.error(f"_save_location_to_profile: {e}", exc_info=True)


# ─── TASDIQLASH ───

async def show_confirm(msg: Message, state: FSMContext):
    d = await state.get_data()
    lang = d.get("user_lang", "uz")
    items = d.get("items", [])
    total = d.get("total", items_total(items))
    addr = d.get("address", "")
    await state.set_state(OrderState.confirming_order)
    await edit_main(
        state, msg.bot,
        get_text("order_confirm_multi", lang,
                 items=format_items_lines(items, lang),
                 total=f"{total:,}", address=addr),
        reply_markup=get_order_confirm_keyboard(lang)
    )


@router.callback_query(OrderState.confirming_order, F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    try:
        d = await state.get_data()
        lang = d.get("user_lang", "uz")
        items = d.get("items", [])
        total = int(d.get("total", items_total(items)))
        total_qty = items_count(items)

        async with get_db() as s:
            user = await crud.get_user_by_telegram_id(s, callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                await state.clear()
                return

            last = await crud.get_last_order_number(s)
            num = last + 1
            order = await crud.create_order(
                s, user_id=user.id, order_number=num,
                quantity=total_qty, address=d.get("address", ""),
                location_lat=d.get("location_lat"), location_lng=d.get("location_lng"),
                items=items_to_json(items), total_price=total
            )

            if DAILY_CHANNEL_ID:
                await send_order_to_channel(callback.bot, s, order, user)

        await edit_main(
            state, callback.bot,
            get_text("order_success_multi", lang, number=f"{num:04d}",
                     items=format_items_lines(items, lang),
                     total=f"{total:,}", address=d.get("address", ""))
        )

        await Stickers.success(callback.bot, callback.from_user.id)
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
        async with get_db() as s:
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
        # Tugma bosilган xabarni yangilash (kanал yoki dostavkachi chati)
        try:
            await callback.message.edit_text(text=t, reply_markup=None)
        except Exception:
            pass
        # Kanал xabarini ham yangilash (dostavkachi chatidан bosilган bo'lsa)
        if DAILY_CHANNEL_ID and order.channel_message_id:
            try:
                await callback.bot.edit_message_text(
                    text=t, chat_id=DAILY_CHANNEL_ID,
                    message_id=order.channel_message_id, reply_markup=None
                )
            except Exception:
                pass
        await callback.answer("✅ Buyurtma yetkazildi deb belgilandi!", show_alert=True)
    except Exception as e:
        logger.error(f"deliver_order: {e}", exc_info=True)
        await callback.answer("Xatolik", show_alert=True)


# ─── DOSTAVKACHIGA YUBORISH ───

@router.callback_query(F.data.startswith("tocourier_"))
async def to_courier_menu(callback: CallbackQuery):
    """Kanalда 'Dostavkachiga yuborish' bosilганда — dostavkachilar ro'yxatini ko'rsatadi."""
    try:
        oid = int(callback.data.split("_")[1])
        if not DELIVERY_STAFF:
            await callback.answer(
                "Dostavkachilar ro'yxati bo'sh.\n.env faylida DELIVERY_STAFF ni to'ldiring.",
                show_alert=True
            )
            return
        b = InlineKeyboardBuilder()
        for cid, name in DELIVERY_STAFF:
            b.button(text=f"🚚 {name}", callback_data=f"sendto_{oid}_{cid}")
        b.button(text="◀️ Orqaga", callback_data=f"backdeliver_{oid}")
        b.adjust(1)
        try:
            await callback.message.edit_reply_markup(reply_markup=b.as_markup())
        except Exception:
            pass
        await callback.answer()
    except Exception as e:
        logger.error(f"to_courier_menu: {e}", exc_info=True)
        await callback.answer("Xatolik", show_alert=True)


@router.callback_query(F.data.startswith("sendto_"))
async def send_to_courier(callback: CallbackQuery):
    """Tanlangan dostavkachiga buyurtmani ishlaydigan 'Yetkazildi' tugmasi bilan yuboradi."""
    try:
        parts = callback.data.split("_")
        oid, cid = int(parts[1]), int(parts[2])

        async with get_db() as s:
            order = await crud.get_order_by_id(s, oid)
            if not order:
                await callback.answer("Buyurtma topilmadi", show_alert=True)
                return
            r = await s.execute(select(User).where(User.id == order.user_id))
            customer = r.scalar_one_or_none()

        name = next((n for i, n in DELIVERY_STAFF if i == cid), str(cid))
        text = "🚚 <b>YANGI YETKAZISH</b>\n\n" + format_order_message(order, customer)

        try:
            if order.location_lat and order.location_lng:
                await callback.bot.send_location(
                    chat_id=cid, latitude=order.location_lat, longitude=order.location_lng
                )
            await callback.bot.send_message(
                chat_id=cid, text=text, reply_markup=get_courier_only_keyboard(order.id)
            )
        except Exception as e:
            logger.warning(f"send_to_courier -> {cid}: {e}")
            await callback.answer(
                f"❌ {name} ga yuborib bo'lmadi.\nU avval botga /start bosishi kerak.",
                show_alert=True
            )
            return

        # Kanal tugmalarini asl holiga qaytaramiz
        try:
            await callback.message.edit_reply_markup(reply_markup=get_deliver_keyboard(order.id))
        except Exception:
            pass
        await callback.answer(f"✅ {name} ga yuborildi!", show_alert=True)
    except Exception as e:
        logger.error(f"send_to_courier: {e}", exc_info=True)
        await callback.answer("Xatolik", show_alert=True)


@router.callback_query(F.data.startswith("backdeliver_"))
async def back_deliver(callback: CallbackQuery):
    """Dostavkachi ro'yxatidан orqaga — asl tugmalarni tiklaydi."""
    try:
        oid = int(callback.data.split("_")[1])
        try:
            await callback.message.edit_reply_markup(reply_markup=get_deliver_keyboard(oid))
        except Exception:
            pass
        await callback.answer()
    except Exception as e:
        logger.error(f"back_deliver: {e}", exc_info=True)
        await callback.answer()


# ─── MENING BUYURTMALARIM ───

@router.message(F.text.in_(["📋 Mening buyurtmalarim", "📋 Мои заказы", "📋 My Orders"]))
async def my_orders(message: Message):
    try:
        async with get_db() as s:
            user = await crud.get_user_by_telegram_id(s, message.from_user.id)
        if not user:
            await message.answer(get_text("please_register", "uz"))
            return

        lang = user.language
        async with get_db() as s:
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

            items = _order_items(o, lang)
            total = o.total_price if o.total_price is not None else (o.quantity * 15000)

            await message.answer(
                f"{si} <b>Buyurtma #{o.order_number:04d}</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"{items}\n"
                f"🏁 Jami: {total:,} so'm\n"
                f"📍 {o.address}\n"
                f"📅 {o.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"🔹 {st}"
            )
    except Exception as e:
        logger.error(f"my_orders: {e}", exc_info=True)


def _order_items(order, lang: str = "uz") -> str:
    """Buyurtma mahsulotlarini matnga formatlaydi (eski buyurtmalar uchun zaxira)."""
    from bot.products import items_from_json
    parsed = items_from_json(order.items)
    if parsed:
        return format_items_lines(parsed, lang)
    # Eski buyurtma (faqat 19 litr, quantity)
    return f"💧 19 litr × {order.quantity} = {order.quantity * 15000:,} so'm"
