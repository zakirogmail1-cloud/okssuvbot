# 🌐 Ko'p Tilli Qo'llab-quvvatlash - Yangilanish

## 📋 Umumiy Ma'lumot
**Sana:** 05.07.2026, 17:30  
**Versiya:** 3.0  
**Tillar:** 🇺🇿 O'zbek | 🇷🇺 Русский | 🇬🇧 English

---

## ✨ Yangi Imkoniyatlar

### 1. **Til Tanlash Sistema**
- ✅ Birinchi start bosganda til tanlash
- ✅ 3 til: O'zbek, Rus, Ingliz
- ✅ Inline klaviatura orqali tanlash
- ✅ Istalgan vaqtda tilni o'zgartirish

### 2. **Klaviaturada Til O'zgartirish**
- ✅ Asosiy menyuda "🌐 Tilni o'zgartirish" tugmasi
- ✅ 3 ta bayroq bilan til tanlash (🇺🇿 🇷🇺 🇬🇧)
- ✅ Tanlangan til avtomatik saqlanadi

### 3. **Barcha Matnlar Tarjima**
- ✅ Xush kelibsiz xabarlari
- ✅ Ro'yxatdan o'tish jarayoni
- ✅ Buyurtma berish  
- ✅ Klaviatura tugmalari
- ✅ Xato xabarlari

---

## 🗂️ Yangi Fayllar

### 1. `bot/localization.py`
Barcha tarjimalarni o'z ichiga olgan asosiy modul.

```python
from bot.localization import get_text

# Foydalanish
text = get_text("welcome_registered", lang="uz", name="Ali")
```

**Imkoniyatlar:**
- `LANGUAGES` - Mavjud tillar ro'yxati
- `TRANSLATIONS` - Barcha tarjimalar
- `get_text(key, lang, **kwargs)` - Matnni olish funksiyasi

---

## 🔄 O'zgargan Fayllar

### 1. **bot/database/models.py**
```python
class User(Base):
    ...
    language = Column(String(2), nullable=False, default="uz")  # YANGI!
```

### 2. **bot/database/connection.py**
```python
async def migrate_schema():
    # language ustuni qo'shildi
    if not await column_exists(conn, "users", "language"):
        await conn.execute(text("ALTER TABLE users ADD COLUMN language VARCHAR(2) NOT NULL DEFAULT 'uz'"))
```

### 3. **bot/database/crud.py**
```python
# Yangi funksiya
async def update_user_language(session: AsyncSession, user_id: int, language: str):
    await session.execute(update(User).where(User.id == user_id).values(language=language))
    await session.commit()
```

### 4. **bot/keyboards/reply.py**
Barcha klaviatura funksiyalariga `lang` parametri qo'shildi:
```python
def get_main_keyboard(lang: str = "uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("btn_order", lang))],
            [KeyboardButton(text=get_text("btn_my_orders", lang))],
            ...
            [KeyboardButton(text=get_text("btn_change_language", lang))],  # YANGI!
        ]
    )
```

### 5. **bot/keyboards/inline.py**
```python
def get_language_inline_keyboard():  # YANGI!
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbek", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    return builder.as_markup()
```

### 6. **bot/handlers/start.py**
- ✅ Til tanlash jarayoni qo'shildi
- ✅ Ro'yxat FSM ga `choosing_language` state qo'shildi
- ✅ Til o'zgartirish handleri qo'shildi
- ✅ Barcha matnlar `get_text()` orqali olindi

---

## 🚀 Qanday Ishlaydi?

### 1. **Yangi Foydalanuvchi:**
```
/start → Til tanlang (inline buttons) → 
  Til tanlandi → 
  Ismingizni kiriting (tanlangan tilda) →
  Telefon raqamingizni kiriting →
  Xonadon hajmini kiriting →
  ✅ Ro'yxatdan o'tdingiz!
```

### 2. **Mavjud Foydalanuvchi:**
```
/start → Xush kelibsiz (o'z tilida)
```

### 3. **Tilni O'zgartirish:**
```
Asosiy menyu → 🌐 Tilni o'zgartirish →
  Til tanlang (inline buttons) →
  ✅ Til o'zgartirildi!
```

---

## 📊 Database Schema

### Users jadvali yangilandi:
```sql
ALTER TABLE users ADD COLUMN language VARCHAR(2) NOT NULL DEFAULT 'uz';
```

**language qiymatlari:**
- `uz` - O'zbek tili (default)
- `ru` - Rus tili
- `en` - Ingliz tili

---

## 🔤 Tarjimalar Ro'yxati

### Asosiy Matnlar:
- `choose_language` - Til tanlash xabari
- `language_changed` - Til o'zgartirildi xabari
- `welcome_registered` - Ro'yxatdan o'tgan foydalanuvchi uchun
- `welcome_new` - Yangi foydalanuvchi uchun
- `enter_name` - Ism so'rash
- `enter_household` - Xonadon hajmi so'rash
- `registration_complete` - Ro'yxatdan o'tish tugadi

### Klaviatura Tugmalari:
- `btn_order` - 🛒 Buyurtma berish
- `btn_my_orders` - 📋 Buyurtmalarim
- `btn_my_info` - 👤 Ma'lumotlarim  
- `btn_support` - 📞 Qo'llab-quvvatlash
- `btn_change_language` - 🌐 Tilni o'zgartirish
- `btn_send_phone` - 📱 Raqamni yuborish
- `btn_send_location` - 📍 Lokatsiya yuborish

### Buyurtma Matnlari:
- `order_start` - Buyurtma boshlash
- `order_quantity` - Soni so'rash
- `order_location` - Manzil so'rash
- `order_confirm` - Buyurtmani tasdiqlash
- `order_success` - Buyurtma muvaffaqiyatli
- `order_cancelled` - Buyurtma bekor qilindi

---

## ✅ Test Scenariylari

### 1. Yangi foydalanuvchi ro'yxatdan o'tish:
```
1. /start → Til tanlash ekrani chiqadi
2. 🇺🇿 O'zbek ni tanlash → O'zbek tilida davom etadi
3. Ismni kiriting → Telefon → Xonadon → ✅ Tayyor
```

### 2. Tilni o'zgartirish:
```
1. 🌐 Tilni o'zgartirish tugmasini bosish
2. 🇷🇺 Русский ni tanlash
3. ✅ Barcha matnlar rus tilida ko'rsatiladi
```

### 3. Buyurtma berish boshqa tilda:
```
1. Tilni 🇬🇧 English ga o'zgartirish
2. 🛒 Place Order ni bosish
3. ✅ Barcha jarayon ingliz tilida
```

---

## 🔧 Migration

Database ni yangilash uchun:
```bash
python -m bot.main
```

Avtomatik migration `users` jadvaliga `language` ustunini qo'shadi.

---

## 📝 Yangi Tarjima Qo'shish

`bot/localization.py` fayliga:
```python
TRANSLATIONS = {
    "yangi_kalit": {
        "uz": "O'zbek tilidagi matn",
        "ru": "Текст на русском языке",
        "en": "Text in English"
    }
}
```

Ishlatish:
```python
from bot.localization import get_text

text = get_text("yangi_kalit", lang="ru")
```

---

## ⚠️ Muhim Eslatmalar

### 1. **Eski Foydalanuvchilar:**
Migration eski foydalanuvchilar uchun avtomatik `uz` tilini o'rnatadi.

### 2. **Default Til:**
Agar til aniqlanmasa, `uz` ishlatiladi.

### 3. **Klaviatura Tugmalari:**
Har bir handler uchun user.language ni olish kerak:
```python
async def my_handler(message: Message):
    async with async_session() as session:
        user = await crud.get_user_by_telegram_id(session, message.from_user.id)
    lang = user.language if user else "uz"
    
    await message.answer(
        get_text("some_key", lang),
        reply_markup=get_main_keyboard(lang)
    )
```

---

## 🎯 Keyingi Qadamlar

### Hali qilinishi kerak:
1. ⏳ `orders.py` handlerini to'liq yangilash
2. ⏳ `admin.py` ga ko'p tilli qo'llab-quvvatlash
3. ⏳ Xato xabarlari uchun tarjimalar
4. ⏳ Kanal xabarlariga til qo'shish

### Taklif etilganlar:
- 📊 Statistikada eng ko'p ishlatiladigan tilni ko'rsatish
- 🔔 Eslatmalarni foydalanuvchi tilida yuborish
- 📧 Admin xabarlari uchun til

---

## 🎉 Natija

✅ **Til tanlash tizimi ishga tushdi!**  
✅ **3 til qo'llab-quvvatlanadi**  
✅ **Klaviaturada til o'zgartirish**  
✅ **Database yangilandi**  
✅ **Tarjimalar fayli yaratildi**

---

**Yaratildi:** 05.07.2026, 17:30  
**Status:** ✅ Tayyor (qisman)  
**Keyingi versiya:** orders.py ni yangilash

Bot endi ko'p tilli! 🌐🎉
