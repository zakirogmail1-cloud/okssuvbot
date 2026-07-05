from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.database.connection import async_session
from bot.database import crud
from bot.keyboards.reply import (
    get_contact_keyboard, get_main_keyboard, get_info_edit_keyboard, get_language_keyboard
)
from bot.keyboards.inline import get_language_inline_keyboard
from bot.localization import get_text
from aiogram.types import ReplyKeyboardRemove

router = Router()


class Registration(StatesGroup):
    choosing_language = State()
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_household_size = State()


class EditInfo(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_new_phone = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)

    if user:
        lang = user.language
        await message.answer(
            get_text("welcome_registered", lang, name=user.full_name),
            reply_markup=get_main_keyboard(lang)
        )
    else:
        # Yangi foydalanuvchi - tilni tanlash
        await message.answer(
            get_text("choose_language", "uz"),
            reply_markup=get_language_inline_keyboard()
        )
        await state.set_state(Registration.choosing_language)


@router.callback_query(Registration.choosing_language, F.data.startswith("lang_"))
async def process_language_choice(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]  # uz, ru, en
    await state.update_data(language=lang)
    
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass
    
    await callback.message.answer(
        get_text("welcome_new", lang)
    )
    await state.set_state(Registration.waiting_for_name)
    await callback.answer()


@router.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    data = await state.get_data()
    lang = data.get("language", "uz")
    
    if len(name) < 3:
        await message.answer(get_text("invalid_name", lang))
        return

    await state.update_data(full_name=name)
    await message.answer(
        get_text("enter_name", lang, name=name.split()[0]),
        reply_markup=get_contact_keyboard(lang)
    )
    await state.set_state(Registration.waiting_for_phone)


@router.message(Registration.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    await state.update_data(phone=phone)
    await ask_household_size(message, state)


@router.message(Registration.waiting_for_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    
    phone = message.text.strip()
    if not phone.startswith("+"):
        phone = "+" + phone
    if len(phone) < 10 or not phone[1:].isdigit():
        await message.answer(get_text("invalid_phone_prompt", lang))
        return
    await state.update_data(phone=phone)
    await ask_household_size(message, state)


async def ask_household_size(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(
        get_text("enter_household", lang),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.waiting_for_household_size)


@router.message(Registration.waiting_for_household_size, F.text.func(lambda t: t.strip().isdigit() and int(t.strip()) > 0))
async def process_household_size(message: Message, state: FSMContext):
    household_size = int(message.text.strip())
    data = await state.get_data()
    lang = data.get("language", "uz")

    async with async_session() as session:
        user = await crud.create_user(
            session,
            telegram_id=message.from_user.id,
            full_name=data["full_name"],
            phone=data["phone"],
            household_size=household_size,
            language=lang
        )

    await message.answer(
        get_text("registration_complete", lang, 
                name=user.full_name, phone=user.phone, household=user.household_size),
        reply_markup=get_main_keyboard(lang)
    )
    await state.clear()


@router.message(Registration.waiting_for_household_size)
async def process_household_size_invalid(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(get_text("invalid_household", lang))


@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Изменить язык", "🌐 Change Language"]))
async def change_language(message: Message):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
    
    if not user:
        await message.answer("💡 Iltimos, avval ro'yxatdan o'ting: /start")
        return
    
    await message.answer(
        get_text("choose_language", user.language),
        reply_markup=get_language_inline_keyboard()
    )


@router.message(F.text.in_(["ℹ️ Biz haqimizda", "ℹ️ О нас", "ℹ️ About Us"]))
async def about_us(message: Message):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
    
    if not user:
        await message.answer("💡 Iltimos, avval ro'yxatdan o'ting: /start")
        return
    
    lang = user.language
    await message.answer(
        get_text("about_us_title", lang) + "\n\n" + get_text("about_us_info", lang),
        reply_markup=get_main_keyboard(lang)
    )


@router.callback_query(F.data.startswith("lang_"))
async def process_language_change(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, callback.from_user.id)
        if user:
            await crud.update_user_language(session, user.id, lang)
    
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass
    
    await callback.message.answer(
        get_text("language_changed", lang),
        reply_markup=get_main_keyboard(lang)
    )
    await callback.answer()


@router.message(F.text.in_(["👤 Mening ma'lumotlarim", "👤 Моя информация", "👤 My Information"]))
async def my_info(message: Message):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)

    if not user:
        await message.answer(get_text("please_register", "uz"))
        return

    lang = user.language
    await message.answer(
        get_text("my_info_title", lang) + "\n\n" + 
        get_text("my_info_text", lang, name=user.full_name, phone=user.phone, household=user.household_size),
        reply_markup=get_info_edit_keyboard(lang)
    )


@router.message(F.text.in_(["✏️ Ismni o'zgartirish", "✏️ Изменить имя", "✏️ Edit Name"]))
async def edit_name_start(message: Message, state: FSMContext):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)

    if not user:
        await message.answer(get_text("please_register", "uz"))
        return

    lang = user.language
    await message.answer(
        get_text("edit_name_prompt", lang),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EditInfo.waiting_for_new_name)


@router.message(EditInfo.waiting_for_new_name)
async def edit_name_process(message: Message, state: FSMContext):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        if user:
            lang = user.language
        else:
            lang = "uz"
    
    if len(message.text.strip()) < 3:
        await message.answer(get_text("invalid_name_short", lang))
        return

    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        if user:
            await crud.update_user_name(session, user.id, message.text.strip())

    await message.answer(
        get_text("name_changed", lang, name=message.text.strip()),
        reply_markup=get_main_keyboard(lang)
    )
    await state.clear()


@router.message(F.text.in_(["✏️ Telefon raqamni o'zgartirish", "✏️ Изменить телефон", "✏️ Edit Phone"]))
async def edit_phone_start(message: Message, state: FSMContext):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)

    if not user:
        await message.answer(get_text("please_register", "uz"))
        return

    lang = user.language
    await message.answer(
        get_text("edit_phone_prompt", lang),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EditInfo.waiting_for_new_phone)


@router.message(EditInfo.waiting_for_new_phone)
async def edit_phone_process(message: Message, state: FSMContext):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        if user:
            lang = user.language
        else:
            lang = "uz"
    
    phone = message.text.strip()
    if not phone.startswith("+"):
        phone = "+" + phone
    if len(phone) < 10 or not phone[1:].isdigit():
        await message.answer(get_text("invalid_phone_format", lang))
        return

    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        if user:
            await crud.update_user_phone(session, user.id, phone)

    await message.answer(
        get_text("phone_changed", lang, phone=phone),
        reply_markup=get_main_keyboard(lang)
    )
    await state.clear()


@router.message(F.text.in_(["📞 Qo'llab-quvvatlash", "📞 Поддержка", "📞 Support"]))
async def support(message: Message):
    from bot.config import ADMIN_TELEGRAM_IDS
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)

    if not user:
        await message.answer(get_text("please_register", "uz"))
        return

    lang = user.language
    username = message.from_user.username or "Noma'lum"
    admin_text = (
        f"📞 <b>MIJOZDAN YORDAM SO'ROVI</b>\n\n"
        f"👤 <b>Ism:</b> {user.full_name}\n"
        f"📞 <b>Telefon:</b> {user.phone}\n"
        f"🆔 <b>Username:</b> @{username}"
    )

    for admin_id in ADMIN_TELEGRAM_IDS:
        try:
            await message.bot.send_message(chat_id=admin_id, text=admin_text)
            await message.bot.forward_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except Exception:
            pass

    await message.answer(
        get_text("support_sent", lang),
        reply_markup=get_main_keyboard(lang)
    )


@router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад", "◀️ Back"]))
async def go_back(message: Message, state: FSMContext):
    await state.clear()
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        lang = user.language if user else "uz"
    
    await message.answer(
        get_text("back_to_menu", lang),
        reply_markup=get_main_keyboard(lang)
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
        lang = user.language if user else "uz"
    
    await message.answer(
        get_text("process_cancelled", lang),
        reply_markup=get_main_keyboard(lang)
    )
