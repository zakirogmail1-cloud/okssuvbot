# -*- coding: utf-8 -*-
"""
Lokalizatsiya tizimi - 3 til: O'zbek, Rus, Ingliz
"""

LANGUAGES = {
    "uz": "🇺🇿 O'zbek",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English"
}

TRANSLATIONS = {
    # Umumiy
    "choose_language": {
        "uz": "🌐 <b>Tilni tanlang:</b>\n\nQuyidagi tillardan birini tanlang:",
        "ru": "🌐 <b>Выберите язык:</b>\n\nВыберите один из следующих языков:",
        "en": "🌐 <b>Choose language:</b>\n\nSelect one of the following languages:"
    },
    "language_changed": {
        "uz": "✅ Til o'zgartirildi: O'zbek tili",
        "ru": "✅ Язык изменен: Русский",
        "en": "✅ Language changed: English"
    },
    
    # Start va ro'yxat
    "welcome_registered": {
        "uz": "🌟 Assalomu alaykum, {name}!\n\n💧 <b>OKS Suv</b> ga xush kelibsiz!\nToza va sifatli ichimlik suvi — sog'lik garovi.",
        "ru": "🌟 Здравствуйте, {name}!\n\n💧 Добро пожаловать в <b>OKS Suv</b>!\nЧистая и качественная питьевая вода — залог здоровья.",
        "en": "🌟 Hello, {name}!\n\n💧 Welcome to <b>OKS Suv</b>!\nClean and quality drinking water — the key to health."
    },
    "welcome_new": {
        "uz": "🌟 <b>Assalomu alaykum!</b>\n\n💧 <b>OKS Suv</b> — Termiz shahrida sifatli ichimlik suvi yetkazib berish xizmati.\n\n🤝 Botdan foydalanish uchun avval ro'yxatdan o'ting.\nIltimos, <b>to'liq ismingizni</b> kiriting:\n\n📌 Masalan: <i>Alisher Karimov</i>",
        "ru": "🌟 <b>Здравствуйте!</b>\n\n💧 <b>OKS Suv</b> — Служба доставки качественной питьевой воды в городе Термез.\n\n🤝 Для использования бота сначала зарегистрируйтесь.\nПожалуйста, введите <b>ваше полное имя</b>:\n\n📌 Например: <i>Алишер Каримов</i>",
        "en": "🌟 <b>Hello!</b>\n\n💧 <b>OKS Suv</b> — Quality drinking water delivery service in Termez.\n\n🤝 To use the bot, please register first.\nPlease enter <b>your full name</b>:\n\n📌 Example: <i>Alisher Karimov</i>"
    },
    "enter_name": {
        "uz": "✅ Rahmat, <b>{name}</b>!\n\n📞 Endi telefon raqamingizni yuboring.\nPastdagi <b>📱 Raqamni yuborish</b> tugmasini bosing.",
        "ru": "✅ Спасибо, <b>{name}</b>!\n\n📞 Теперь отправьте ваш номер телефона.\nНажмите кнопку <b>📱 Отправить номер</b> ниже.",
        "en": "✅ Thank you, <b>{name}</b>!\n\n📞 Now send your phone number.\nPress the <b>📱 Send number</b> button below."
    },
    "invalid_name": {
        "uz": "❌ Iltimos, ismingizni to'g'ri kiriting (kamida 3 harf).\nMasalan: <i>Alisher Karimov</i>",
        "ru": "❌ Пожалуйста, введите ваше имя правильно (минимум 3 буквы).\nНапример: <i>Алишер Каримов</i>",
        "en": "❌ Please enter your name correctly (at least 3 letters).\nExample: <i>Alisher Karimov</i>"
    },
    "enter_household": {
        "uz": "🏠 <b>Xonadoningizda necha kishi yashaydi?</b>\n\nRaqam yozing, masalan: <i>4</i>\n\n💡 Bu ma'lumot sizga eng mos xizmatni taklif qilish uchun kerak.",
        "ru": "🏠 <b>Сколько человек проживает в вашей семье?</b>\n\nНапишите число, например: <i>4</i>\n\n💡 Эта информация нужна для предложения наиболее подходящего сервиса.",
        "en": "🏠 <b>How many people live in your household?</b>\n\nWrite a number, for example: <i>4</i>\n\n💡 This information is needed to offer the most suitable service."
    },
    "registration_complete": {
        "uz": "🎉 <b>Tabriklaymiz! Ro'yxatdan o'tdingiz!</b>\n\n👤 <b>Ism:</b> {name}\n📞 <b>Telefon:</b> {phone}\n🏠 <b>Xonadon:</b> {household} kishi\n\n💧 Endi <b>Buyurtma berish</b> tugmasi orqali suv buyurtma qilishingiz mumkin!\n\n<i>OKS Suv — toza suv, sog' hayot!</i>",
        "ru": "🎉 <b>Поздравляем! Вы зарегистрированы!</b>\n\n👤 <b>Имя:</b> {name}\n📞 <b>Телефон:</b> {phone}\n🏠 <b>Семья:</b> {household} чел.\n\n💧 Теперь вы можете заказать воду через кнопку <b>Заказать</b>!\n\n<i>OKS Suv — чистая вода, здоровая жизнь!</i>",
        "en": "🎉 <b>Congratulations! You are registered!</b>\n\n👤 <b>Name:</b> {name}\n📞 <b>Phone:</b> {phone}\n🏠 <b>Household:</b> {household} people\n\n💧 Now you can order water via the <b>Place Order</b> button!\n\n<i>OKS Suv — clean water, healthy life!</i>"
    },
    "invalid_household": {
        "uz": "❌ Iltimos, faqat musbat raqam kiriting.\nMasalan: <i>4</i>",
        "ru": "❌ Пожалуйста, введите только положительное число.\nНапример: <i>4</i>",
        "en": "❌ Please enter only a positive number.\nExample: <i>4</i>"
    },
    
    # Klaviatura tugmalari
    "btn_order": {
        "uz": "🛒 Buyurtma berish",
        "ru": "🛒 Заказать",
        "en": "🛒 Place Order"
    },
    "btn_my_orders": {
        "uz": "📋 Mening buyurtmalarim",
        "ru": "📋 Мои заказы",
        "en": "📋 My Orders"
    },
    "btn_my_info": {
        "uz": "👤 Mening ma'lumotlarim",
        "ru": "👤 Моя информация",
        "en": "👤 My Information"
    },
    "btn_support": {
        "uz": "📞 Operator bilan bog'lanish",
        "ru": "📞 Связаться с оператором",
        "en": "📞 Contact Operator"
    },
    "btn_change_language": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Изменить язык",
        "en": "🌐 Change Language"
    },
    "btn_about_us": {
        "uz": "ℹ️ Biz haqimizda",
        "ru": "ℹ️ О нас",
        "en": "ℹ️ About Us"
    },
    "btn_send_phone": {
        "uz": "📱 Raqamni yuborish",
        "ru": "📱 Отправить номер",
        "en": "📱 Send Number"
    },
    "btn_send_location": {
        "uz": "📍 Lokatsiya yuborish",
        "ru": "📍 Отправить локацию",
        "en": "📍 Send Location"
    },
    "btn_back": {
        "uz": "◀️ Orqaga",
        "ru": "◀️ Назад",
        "en": "◀️ Back"
    },
    "btn_confirm": {
        "uz": "✅ Tasdiqlash",
        "ru": "✅ Подтвердить",
        "en": "✅ Confirm"
    },
    "btn_cancel": {
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отменить",
        "en": "❌ Cancel"
    },
    "btn_edit_name": {
        "uz": "✏️ Ismni o'zgartirish",
        "ru": "✏️ Изменить имя",
        "en": "✏️ Edit Name"
    },
    "btn_edit_phone": {
        "uz": "✏️ Telefon raqamni o'zgartirish",
        "ru": "✏️ Изменить телефон",
        "en": "✏️ Edit Phone"
    },
    
    # Ma'lumotlar sahifasi
    "my_info_title": {
        "uz": "👤 <b>SIZNING MA'LUMOTLARINGIZ</b>",
        "ru": "👤 <b>ВАША ИНФОРМАЦИЯ</b>",
        "en": "👤 <b>YOUR INFORMATION</b>"
    },
    "my_info_text": {
        "uz": "━━━━━━━━━━━━━━━━━━\n🧑 <b>Ism:</b> {name}\n📞 <b>Telefon:</b> {phone}\n🏠 <b>Xonadon:</b> {household} kishi\n━━━━━━━━━━━━━━━━━━\n\n✏️ Ma'lumotlarni o'zgartirish uchun quyidagi tugmalardan foydalaning:",
        "ru": "━━━━━━━━━━━━━━━━━━\n🧑 <b>Имя:</b> {name}\n📞 <b>Телефон:</b> {phone}\n🏠 <b>Семья:</b> {household} чел.\n━━━━━━━━━━━━━━━━━━\n\n✏️ Для изменения информации используйте кнопки ниже:",
        "en": "━━━━━━━━━━━━━━━━━━\n🧑 <b>Name:</b> {name}\n📞 <b>Phone:</b> {phone}\n🏠 <b>Household:</b> {household} people\n━━━━━━━━━━━━━━━━━━\n\n✏️ To change information, use the buttons below:"
    },
    "edit_name_prompt": {
        "uz": "✏️ <b>Yangi ismingizni kiriting:</b>\n\nMasalan: <i>Akbar Tursunov</i>",
        "ru": "✏️ <b>Введите ваше новое имя:</b>\n\nНапример: <i>Акбар Турсунов</i>",
        "en": "✏️ <b>Enter your new name:</b>\n\nExample: <i>Akbar Tursunov</i>"
    },
    "edit_phone_prompt": {
        "uz": "✏️ <b>Yangi telefon raqamingizni kiriting:</b>\n\nFormat: <b>+998XXXXXXXXX</b>\nMasalan: <i>+998901234567</i>",
        "ru": "✏️ <b>Введите ваш новый номер телефона:</b>\n\nФормат: <b>+998XXXXXXXXX</b>\nНапример: <i>+998901234567</i>",
        "en": "✏️ <b>Enter your new phone number:</b>\n\nFormat: <b>+998XXXXXXXXX</b>\nExample: <i>+998901234567</i>"
    },
    "name_changed": {
        "uz": "✅ <b>Ism o'zgartirildi!</b>\n\nYangi ism: {name}",
        "ru": "✅ <b>Имя изменено!</b>\n\nНовое имя: {name}",
        "en": "✅ <b>Name changed!</b>\n\nNew name: {name}"
    },
    "phone_changed": {
        "uz": "✅ <b>Telefon raqam o'zgartirildi!</b>\n\nYangi raqam: {phone}",
        "ru": "✅ <b>Номер телефона изменен!</b>\n\nНовый номер: {phone}",
        "en": "✅ <b>Phone number changed!</b>\n\nNew number: {phone}"
    },
    "support_sent": {
        "uz": "📞 <b>Qo'llab-quvvatlash</b>\n\nMurojaatingiz <b>admin</b> ga yuborildi.\nTez orada siz bilan bog'lanamiz. ✅\n\n☎️ Bog'lanish uchun: <b>+998 99 058 22 22</b>\n\nKutib qolganingiz uchun rahmat! 😊",
        "ru": "📞 <b>Поддержка</b>\n\nВаше обращение отправлено <b>администратору</b>.\nМы свяжемся с вами в ближайшее время. ✅\n\n☎️ Для связи: <b>+998 99 058 22 22</b>\n\nСпасибо за ожидание! 😊",
        "en": "📞 <b>Support</b>\n\nYour request has been sent to <b>admin</b>.\nWe will contact you soon. ✅\n\n☎️ Contact us: <b>+998 99 058 22 22</b>\n\nThank you for waiting! 😊"
    },
    "operator_contact": {
        "uz": "📞 <b>Operator bilan bog'lanish</b>\n\nQuyidagi raqamga bosib qo'ng'iroq qiling:\n☎️ <b>+998 99 058 22 22</b>\n\nOperatorlarimiz siz bilan bog'lanishga tayyor. 😊",
        "ru": "📞 <b>Связаться с оператором</b>\n\nНажмите на номер ниже, чтобы позвонить:\n☎️ <b>+998 99 058 22 22</b>\n\nНаши операторы готовы связаться с вами. 😊",
        "en": "📞 <b>Contact Operator</b>\n\nTap the number below to call:\n☎️ <b>+998 99 058 22 22</b>\n\nOur operators are ready to assist you. 😊"
    },
    "operator_contact_error": {
        "uz": "⚠️ <b>Xatolik yuz berdi</b>\n\nOperator bilan bog'lanish ma'lumotlarini yuborib bo'lmadi.\nIltimos, birozdan so'ng qayta urinib ko'ring. 🙏",
        "ru": "⚠️ <b>Произошла ошибка</b>\n\nНе удалось отправить контактные данные оператора.\nПожалуйста, попробуйте ещё раз чуть позже. 🙏",
        "en": "⚠️ <b>Something went wrong</b>\n\nWe couldn't deliver the operator contact details.\nPlease try again in a moment. 🙏"
    },
    "back_to_menu": {
        "uz": "🏠 <b>Bosh menyu</b>\n\nQuyidagi tugmalardan birini tanlang:",
        "ru": "🏠 <b>Главное меню</b>\n\nВыберите одну из кнопок ниже:",
        "en": "🏠 <b>Main menu</b>\n\nSelect one of the buttons below:"
    },
    "process_cancelled": {
        "uz": "🚫 Jarayon bekor qilindi.\n\n🏠 Bosh menyuga qaytdingiz.",
        "ru": "🚫 Процесс отменен.\n\n🏠 Вы вернулись в главное меню.",
        "en": "🚫 Process cancelled.\n\n🏠 You returned to the main menu."
    },
    "please_register": {
        "uz": "💡 Iltimos, avval ro'yxatdan o'ting: /start",
        "ru": "💡 Пожалуйста, сначала зарегистрируйтесь: /start",
        "en": "💡 Please register first: /start"
    },
    "invalid_name_short": {
        "uz": "❌ Iltimos, to'liq ismingizni kiriting (kamida 3 harf).",
        "ru": "❌ Пожалуйста, введите ваше полное имя (минимум 3 буквы).",
        "en": "❌ Please enter your full name (at least 3 letters)."
    },
    "invalid_phone_format": {
        "uz": "❌ Noto'g'ri format. Iltimos, <b>+998XXXXXXXXX</b> shaklida yozing.",
        "ru": "❌ Неверный формат. Пожалуйста, введите в формате <b>+998XXXXXXXXX</b>.",
        "en": "❌ Invalid format. Please enter in format <b>+998XXXXXXXXX</b>."
    },
    "invalid_phone_prompt": {
        "uz": "❌ Noto'g'ri format.\nIltimos, <b>+998XXXXXXXXX</b> shaklida yozing yoki\n📱 Raqamni yuborish tugmasini bosing.",
        "ru": "❌ Неверный формат.\nПожалуйста, введите в формате <b>+998XXXXXXXXX</b> или\nнажмите кнопку 📱 Отправить номер.",
        "en": "❌ Invalid format.\nPlease enter in format <b>+998XXXXXXXXX</b> or\npress the 📱 Send number button."
    },
    
    # Buyurtma berish
    "order_start": {
        "uz": "🛒 <b>Buyurtma berish</b>\n\nQuyidagi mahsulotlardan birini tanlang:",
        "ru": "🛒 <b>Оформление заказа</b>\n\nВыберите один из следующих товаров:",
        "en": "🛒 <b>Place Order</b>\n\nSelect one of the following products:"
    },
    "order_active_warning": {
        "uz": "⚠️ <b>Diqqat!</b>\n\nSizda allaqachon <b>aktiv buyurtma</b> mavjud.\nAvvalgi buyurtma yetkazib berilgach, yangi buyurtma berishingiz mumkin.\n\nRahmat! 😊",
        "ru": "⚠️ <b>Внимание!</b>\n\nУ вас уже есть <b>активный заказ</b>.\nПосле доставки предыдущего заказа вы сможете сделать новый.\n\nСпасибо! 😊",
        "en": "⚠️ <b>Attention!</b>\n\nYou already have an <b>active order</b>.\nAfter the previous order is delivered, you can place a new one.\n\nThank you! 😊"
    },
    "order_quantity": {
        "uz": "🔢 <b>Nechta 19 litrlik kerak?</b>\n\nFaqat raqam yozing.\nMasalan: <i>2</i>",
        "ru": "🔢 <b>Сколько 19-литровых бутылок нужно?</b>\n\nНапишите только число.\nНапример: <i>2</i>",
        "en": "🔢 <b>How many 19-liter bottles do you need?</b>\n\nWrite only a number.\nExample: <i>2</i>"
    },
    "order_location": {
        "uz": "📍 <b>Manzil ma'lumotlari</b>\n\nIltimos, pastdagi tugma orqali <b>lokatsiya</b> yuboring\nyoki manzilingizni matn shaklida yozib yuboring.\n\n📌 Masalan: <i>Ko'cha, uy raqami, kvartira</i>",
        "ru": "📍 <b>Информация об адресе</b>\n\nПожалуйста, отправьте <b>локацию</b> через кнопку ниже\nили напишите ваш адрес текстом.\n\n📌 Например: <i>Улица, номер дома, квартира</i>",
        "en": "📍 <b>Address Information</b>\n\nPlease send your <b>location</b> via the button below\nor write your address as text.\n\n📌 Example: <i>Street, house number, apartment</i>"
    },
    "order_location_prompt": {
        "uz": "📍 Lokatsiyangizni yuboring yoki manzilni yozing:",
        "ru": "📍 Отправьте вашу локацию или напишите адрес:",
        "en": "📍 Send your location or write the address:"
    },
    "order_address": {
        "uz": "✅ Lokatsiya qabul qilindi!\n\n✍️ Endi <b>aniq manzilingizni</b> yozing:\n\n📌 <i>Ko'cha, uy raqami, kvartira, mo'ljal</i>",
        "ru": "✅ Локация принята!\n\n✍️ Теперь напишите <b>точный адрес</b>:\n\n📌 <i>Улица, номер дома, квартира, ориентир</i>",
        "en": "✅ Location received!\n\n✍️ Now write your <b>exact address</b>:\n\n📌 <i>Street, house number, apartment, landmark</i>"
    },
    "order_confirm": {
        "uz": "📋 <b>BUYURTMANGIZNI TEKSHIRING</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n💧 <b>Mahsulot:</b> 19 litr — 15 000 so'm\n🔢 <b>Soni:</b> {quantity} ta\n🏁 <b>Jami:</b> {total} so'm\n📍 <b>Manzil:</b> {address}\n━━━━━━━━━━━━━━━━━━━━━━\n\n👇 Pastdagi tugmalar orqali tasdiqlang yoki bekor qiling:",
        "ru": "📋 <b>ПРОВЕРЬТЕ ВАШ ЗАКАЗ</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n💧 <b>Товар:</b> 19 литров — 15 000 сум\n🔢 <b>Количество:</b> {quantity} шт.\n🏁 <b>Итого:</b> {total} сум\n📍 <b>Адрес:</b> {address}\n━━━━━━━━━━━━━━━━━━━━━━\n\n👇 Подтвердите или отмените через кнопки ниже:",
        "en": "📋 <b>CHECK YOUR ORDER</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n💧 <b>Product:</b> 19 liters — 15,000 sum\n🔢 <b>Quantity:</b> {quantity} pcs\n🏁 <b>Total:</b> {total} sum\n📍 <b>Address:</b> {address}\n━━━━━━━━━━━━━━━━━━━━━━\n\n👇 Confirm or cancel using the buttons below:"
    },
    "order_success": {
        "uz": "✅ <b>Buyurtma qabul qilindi!</b> 🎉\n\n📦 <b>Kun davomida yetqazib beriladi.</b>\n\n📋 <b>Buyurtma raqami:</b> #{number}\n💧 <b>Mahsulot:</b> 19 litr × {quantity}\n📍 <b>Manzil:</b> {address}\n\n🙏 Biz bilan bo'lganingiz uchun rahmat!\n<i>OKS Suv — toza suv, sog' hayot!</i> 💧",
        "ru": "✅ <b>Заказ принят!</b> 🎉\n\n📦 <b>Доставка в течение дня.</b>\n\n📋 <b>Номер заказа:</b> #{number}\n💧 <b>Товар:</b> 19 литров × {quantity}\n📍 <b>Адрес:</b> {address}\n\n🙏 Спасибо, что выбрали нас!\n<i>OKS Suv — чистая вода, здоровая жизнь!</i> 💧",
        "en": "✅ <b>Order accepted!</b> 🎉\n\n📦 <b>Delivery within the day.</b>\n\n📋 <b>Order number:</b> #{number}\n💧 <b>Product:</b> 19 liters × {quantity}\n📍 <b>Address:</b> {address}\n\n🙏 Thank you for choosing us!\n<i>OKS Suv — clean water, healthy life!</i> 💧"
    },
    "order_cancelled": {
        "uz": "🚫 <b>Buyurtma bekor qilindi.</b>\n\nYangi buyurtma berish uchun 🛒 Buyurtma berish tugmasini bosing.\n\n🏠 Bosh menyu",
        "ru": "🚫 <b>Заказ отменен.</b>\n\nДля нового заказа нажмите кнопку 🛒 Заказать.\n\n🏠 Главное меню",
        "en": "🚫 <b>Order cancelled.</b>\n\nTo place a new order, press 🛒 Place Order button.\n\n🏠 Main menu"
    },
    "main_menu": {
        "uz": "🏠 Bosh menyu",
        "ru": "🏠 Главное меню",
        "en": "🏠 Main menu"
    },
    "product_19l": {
        "uz": "💧 19 litr — 15 000 so'm",
        "ru": "💧 19 литров — 15 000 сум",
        "en": "💧 19 liters — 15,000 sum"
    },
    "product_cancel": {
        "uz": "◀️ Bekor qilish",
        "ru": "◀️ Отменить",
        "en": "◀️ Cancel"
    },
    "invalid_quantity": {
        "uz": "❌ Iltimos, faqat musbat raqam kiriting.\nMasalan: <i>2</i>",
        "ru": "❌ Пожалуйста, введите только положительное число.\nНапример: <i>2</i>",
        "en": "❌ Please enter only a positive number.\nExample: <i>2</i>"
    },
    "invalid_location": {
        "uz": "📍 Iltimos, <b>lokatsiya</b> yuboring yoki manzilingizni kamida 5 belgida yozing.",
        "ru": "📍 Пожалуйста, отправьте <b>локацию</b> или напишите ваш адрес минимум из 5 символов.",
        "en": "📍 Please send your <b>location</b> or write your address with at least 5 characters."
    },
    "invalid_address": {
        "uz": "❌ Manzil juda qisqa.\n\nIltimos, to'liq manzilni kiriting:\n📌 <i>Ko'cha, uy raqami, kvartira</i>",
        "ru": "❌ Адрес слишком короткий.\n\nПожалуйста, введите полный адрес:\n📌 <i>Улица, номер дома, квартира</i>",
        "en": "❌ Address is too short.\n\nPlease enter the full address:\n📌 <i>Street, house number, apartment</i>"
    },
    "order_error": {
        "uz": "❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
        "ru": "❌ Произошла ошибка. Попробуйте еще раз.",
        "en": "❌ An error occurred. Please try again."
    },
    
    # Mening buyurtmalarim
    "my_orders_title": {
        "uz": "📋 <b>Mening buyurtmalarim</b> (oxirgi 10 ta):",
        "ru": "📋 <b>Мои заказы</b> (последние 10):",
        "en": "📋 <b>My Orders</b> (last 10):"
    },
    "my_orders_empty": {
        "uz": "📋 <b>Buyurtmalarim</b>\n\nSizda hali buyurtmalar mavjud emas.\n🛒 <b>Buyurtma berish</b> tugmasi orqali birinchi buyurtmangizni bering!",
        "ru": "📋 <b>Мои заказы</b>\n\nУ вас пока нет заказов.\nОформите свой первый заказ через кнопку 🛒 <b>Заказать</b>!",
        "en": "📋 <b>My Orders</b>\n\nYou don't have any orders yet.\nPlace your first order via the 🛒 <b>Place Order</b> button!"
    },
    "order_status_delivered": {
        "uz": "✅ Yetkazib berilgan",
        "ru": "✅ Доставлен",
        "en": "✅ Delivered"
    },
    "order_status_pending": {
        "uz": "⏳ Yetkazilmoqda",
        "ru": "⏳ Доставляется",
        "en": "⏳ In delivery"
    },
    
    # Biz haqimizda
    "about_us_title": {
        "uz": "ℹ️ <b>BIZ HAQIMIZDA</b>",
        "ru": "ℹ️ <b>О НАС</b>",
        "en": "ℹ️ <b>ABOUT US</b>"
    },
    "about_us_info": {
        "uz": """
💧 <b>OKS SUVLARI</b> — bu har bir xonadon va tashkilot uchun sifatli, toza hamda ishonchli ichimlik suvi yetkazib beruvchi brend.

Biz mijozlarimizga yuqori sifat standartlariga javob beradigan ichimlik suvini zamonaviy texnologiyalar asosida yetkazib berishni o'z oldimizga maqsad qilganmiz.

✅ Toza va sifatli ichimlik suvi
🚚 Tezkor va ishonchli yetkazib berish
🏢 Uylar, ofislar, korxonalar va tashkilotlar uchun xizmat
🤝 Har bir mijozga mas'uliyat va e'tibor bilan yondashuv

Bizning asosiy maqsadimiz — har bir xonadonga toza suv va sifatli xizmatni yetkazish.

🌐 <b>Rasmiy saytimiz:</b> https://www.okssuvlari.uz/
Saytimiz orqali mahsulotlarimiz, narxlarimiz va xizmatlarimiz haqida batafsil ma'lumot olishingiz mumkin.

💙 <b>OKS SUVLARI — Tozalik, sifat va ishonch bir manzilda!</b>
""",
        "ru": """
💧 <b>OKS SUVLARI</b> — это бренд по доставке качественной, чистой и надёжной питьевой воды для каждого дома и организации.

Мы поставили перед собой цель доставлять питьевую воду, отвечающую высоким стандартам качества, на основе современных технологий.

✅ Чистая и качественная питьевая вода
🚚 Быстрая и надёжная доставка
🏢 Обслуживание домов, офисов, предприятий и организаций
🤝 Ответственный и внимательный подход к каждому клиенту

Наша главная цель — доставить чистую воду и качественный сервис в каждый дом.

🌐 <b>Наш официальный сайт:</b> https://www.okssuvlari.uz/
На сайте вы можете получить подробную информацию о нашей продукции, ценах и услугах.

💙 <b>OKS SUVLARI — Чистота, качество и доверие в одном месте!</b>
""",
        "en": """
💧 <b>OKS SUVLARI</b> is a brand delivering quality, clean and reliable drinking water for every home and organization.

Our goal is to deliver drinking water that meets high quality standards using modern technologies.

✅ Clean and quality drinking water
🚚 Fast and reliable delivery
🏢 Service for homes, offices, businesses and organizations
🤝 A responsible and attentive approach to every customer

Our main goal is to bring clean water and quality service to every home.

🌐 <b>Our official website:</b> https://www.okssuvlari.uz/
Through our website you can get detailed information about our products, prices and services.

💙 <b>OKS SUVLARI — Cleanliness, quality and trust in one place!</b>
"""
    },

    # ── Yangi buyurtma oqimi (bir nechta mahsulot) ──
    "order_choose_products": {
        "uz": "🛒 <b>Mahsulotlarni tanlang</b>\n\nHar bir mahsulot yonidagi ➕ / ➖ tugmalari orqali sonini belgilang.\nTayyor bo'lgach, <b>✅ Davom etish</b> tugmasini bosing.",
        "ru": "🛒 <b>Выберите товары</b>\n\nУкажите количество кнопками ➕ / ➖ рядом с каждым товаром.\nКогда будете готовы, нажмите <b>✅ Продолжить</b>.",
        "en": "🛒 <b>Choose products</b>\n\nSet the quantity with the ➕ / ➖ buttons next to each product.\nWhen ready, press <b>✅ Continue</b>."
    },
    "cart_summary": {
        "uz": "🛒 Savat (jami): {total} so'm",
        "ru": "🛒 Корзина (итого): {total} сум",
        "en": "🛒 Cart (total): {total} sum"
    },
    "btn_continue": {
        "uz": "✅ Davom etish",
        "ru": "✅ Продолжить",
        "en": "✅ Continue"
    },
    "cart_empty": {
        "uz": "❌ Kamida bitta mahsulot tanlang (➕ tugmasini bosing).",
        "ru": "❌ Выберите хотя бы один товар (нажмите ➕).",
        "en": "❌ Select at least one product (press ➕)."
    },
    "order_confirm_multi": {
        "uz": "📋 <b>BUYURTMANGIZNI TEKSHIRING</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n{items}\n━━━━━━━━━━━━━━━━━━━━━━\n🏁 <b>Jami:</b> {total} so'm\n📍 <b>Manzil:</b> {address}\n━━━━━━━━━━━━━━━━━━━━━━\n\n👇 Tasdiqlang yoki bekor qiling:",
        "ru": "📋 <b>ПРОВЕРЬТЕ ВАШ ЗАКАЗ</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n{items}\n━━━━━━━━━━━━━━━━━━━━━━\n🏁 <b>Итого:</b> {total} сум\n📍 <b>Адрес:</b> {address}\n━━━━━━━━━━━━━━━━━━━━━━\n\n👇 Подтвердите или отмените:",
        "en": "📋 <b>CHECK YOUR ORDER</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n{items}\n━━━━━━━━━━━━━━━━━━━━━━\n🏁 <b>Total:</b> {total} sum\n📍 <b>Address:</b> {address}\n━━━━━━━━━━━━━━━━━━━━━━\n\n👇 Confirm or cancel:"
    },
    "order_success_multi": {
        "uz": "✅ <b>Buyurtma qabul qilindi!</b> 🎉\n\n📦 <b>Kun davomida yetkazib beriladi.</b>\n\n📋 <b>Buyurtma raqami:</b> #{number}\n{items}\n🏁 <b>Jami:</b> {total} so'm\n📍 <b>Manzil:</b> {address}\n\n🙏 Biz bilan bo'lganingiz uchun rahmat!\n<i>OKS Suv — toza suv, sog' hayot!</i> 💧",
        "ru": "✅ <b>Заказ принят!</b> 🎉\n\n📦 <b>Доставка в течение дня.</b>\n\n📋 <b>Номер заказа:</b> #{number}\n{items}\n🏁 <b>Итого:</b> {total} сум\n📍 <b>Адрес:</b> {address}\n\n🙏 Спасибо, что выбрали нас!\n<i>OKS Suv — чистая вода, здоровая жизнь!</i> 💧",
        "en": "✅ <b>Order accepted!</b> 🎉\n\n📦 <b>Delivery within the day.</b>\n\n📋 <b>Order number:</b> #{number}\n{items}\n🏁 <b>Total:</b> {total} sum\n📍 <b>Address:</b> {address}\n\n🙏 Thank you for choosing us!\n<i>OKS Suv — clean water, healthy life!</i> 💧"
    },
    "order_using_saved_address": {
        "uz": "📍 <b>Yetkazib berish manzili:</b>\n{address}\n\n<i>(Manzilni «Mening ma'lumotlarim» bo'limidan o'zgartirishingiz mumkin.)</i>",
        "ru": "📍 <b>Адрес доставки:</b>\n{address}\n\n<i>(Адрес можно изменить в разделе «Моя информация».)</i>",
        "en": "📍 <b>Delivery address:</b>\n{address}\n\n<i>(You can change the address in «My Information».)</i>"
    },

    # ── Manzilni o'zgartirish ──
    "btn_edit_address": {
        "uz": "📍 Manzilni o'zgartirish",
        "ru": "📍 Изменить адрес",
        "en": "📍 Edit Address"
    },
    "btn_edit_household": {
        "uz": "🏠 Xonadon sonini o'zgartirish",
        "ru": "🏠 Изменить кол-во человек",
        "en": "🏠 Edit Household Size"
    },
    "edit_household_prompt": {
        "uz": "🏠 <b>Xonadoningizda necha kishi yashaydi?</b>\n\nRaqam yozing, masalan: <i>4</i>",
        "ru": "🏠 <b>Сколько человек проживает в вашей семье?</b>\n\nНапишите число, например: <i>4</i>",
        "en": "🏠 <b>How many people live in your household?</b>\n\nWrite a number, for example: <i>4</i>"
    },
    "household_changed": {
        "uz": "✅ <b>Xonadon soni o'zgartirildi!</b>\n\n🏠 Yangi son: {household} kishi",
        "ru": "✅ <b>Количество человек изменено!</b>\n\n🏠 Новое число: {household} чел.",
        "en": "✅ <b>Household size changed!</b>\n\n🏠 New size: {household} people"
    },
    "edit_address_prompt": {
        "uz": "📍 <b>Yangi manzilingizni yuboring:</b>\n\nPastdagi tugma orqali <b>lokatsiya</b> yuboring yoki manzilni matn shaklida yozing.\n\n📌 Masalan: <i>Ko'cha, uy raqami, kvartira</i>",
        "ru": "📍 <b>Отправьте новый адрес:</b>\n\nОтправьте <b>локацию</b> через кнопку ниже или напишите адрес текстом.\n\n📌 Например: <i>Улица, номер дома, квартира</i>",
        "en": "📍 <b>Send your new address:</b>\n\nSend a <b>location</b> via the button below or write the address as text.\n\n📌 Example: <i>Street, house number, apartment</i>"
    },
    "address_changed": {
        "uz": "✅ <b>Manzil o'zgartirildi!</b>\n\n📍 Yangi manzil: {address}",
        "ru": "✅ <b>Адрес изменен!</b>\n\n📍 Новый адрес: {address}",
        "en": "✅ <b>Address changed!</b>\n\n📍 New address: {address}"
    },
    "no_saved_address": {
        "uz": "kiritilmagan",
        "ru": "не указан",
        "en": "not set"
    },
    "my_info_address_line": {
        "uz": "📍 <b>Manzil:</b> {address}\n",
        "ru": "📍 <b>Адрес:</b> {address}\n",
        "en": "📍 <b>Address:</b> {address}\n"
    }
}


def get_text(key: str, lang: str = "uz", **kwargs) -> str:
    """Matnni olish"""
    text = TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get("uz", key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text
