# ℹ️ Biz Haqimizda - Yangi Funksiya

## 📋 Umumiy Ma'lumot
**Sana:** 05.07.2026, 18:45  
**Funksiya:** Biz haqimizda sahifasi  
**Klaviatura:** 2 ustunli (3+3 tugma)

---

## ✨ Nima Qo'shildi?

### 1. **Yangi Tugma - "ℹ️ Biz haqimizda"**
Asosiy klaviaturaga yangi tugma qo'shildi - bu orqali foydalanuvchilar kompaniya haqida ma'lumot, aksiyalar va afzalliklarni ko'rishlari mumkin.

### 2. **2 Ustunli Klaviatura (3+3)**
Klaviatura endi 2 ustunli va 6 ta tugma:

```
┌─────────────────────────────────────┐
│  🛒 Buyurtma      │  📋 Buyurtmalarim │
│     berish        │                   │
├─────────────────────────────────────┤
│  👤 Mening        │  ℹ️ Biz haqimizda │
│  ma'lumotlarim    │                   │
├─────────────────────────────────────┤
│  📞 Qo'llab-      │  🌐 Tilni         │
│  quvvatlash       │  o'zgartirish     │
└─────────────────────────────────────┘
```

### 3. **Ko'p Tilda Qo'llab-quvvatlash**
"Biz haqimizda" sahifasi 3 tilda:
- 🇺🇿 O'zbek
- 🇷🇺 Rus
- 🇬🇧 Ingliz

---

## 📄 "Biz Haqimizda" Sahifasi

### Nima Mavjud?

#### 1. **Kompaniya Ma'lumotlari** 🏢
```
OKS Suv — Termiz shahrida faoliyat 
yurituvchi yetakchi ichimlik suvi 
yetkazib berish xizmati.

📍 Manzil: Termiz shahri, O'zbekiston
📞 Telefon: +998 XX XXX XX XX
🕐 Ish vaqti: Har kuni: 08:00 - 22:00
```

#### 2. **Bizning Afzalliklarimiz** ✅
```
✅ Toza va sifatli suv
   100% sertifikatlangan mahsulot

✅ Tez yetkazib berish
   Kun davomida yetkazamiz

✅ Arzon narxlar
   19 litr — atiga 15 000 so'm

✅ Ishonchli xizmat
   Yillar davomida mijozlarimiz 
   ishonchini qozonganmiz
```

#### 3. **Joriy Aksiyalar** 🎉
```
🔥 Yangi mijozlar uchun:
   Birinchi buyurtmaga 10% chegirma!

🔥 Katta buyurtmalar:
   5 dona va undan ko'p — 
   BEPUL yetkazib berish!

🔥 Doimiy mijozlar:
   Har 10-buyurtmaga bonus!
```

---

## 🎨 Klaviatura Dizayni

### Eski Dizayn (1 ustun):
```
┌─────────────────────┐
│  🛒 Buyurtma berish │
├─────────────────────┤
│  📋 Buyurtmalarim   │
├─────────────────────┤
│  👤 Ma'lumotlarim   │
├─────────────────────┤
│  📞 Qo'llab-quvvat  │
├─────────────────────┤
│  🌐 Tilni o'zgartir │
└─────────────────────┘
```

### Yangi Dizayn (2 ustun):
```
┌───────────────────────────┐
│  🛒 Buyurtma │  📋 Buyurtma│
│     berish   │     larim   │
├───────────────────────────┤
│  👤 Mening   │  ℹ️ Biz     │
│  ma'lumotim  │  haqimizda  │
├───────────────────────────┤
│  📞 Qo'llab- │  🌐 Tilni   │
│  quvvatlash  │  o'zgartir  │
└───────────────────────────┘
```

**Afzalliklari:**
- ✅ Ixcham va zamonaviy
- ✅ Ekranda kam joy egallaydi
- ✅ 6 ta tugma bir nazar ostida
- ✅ Mobil qurilmalarda qulay

---

## 🔄 Qanday Ishlaydi?

### 1. Foydalanuvchi Tomonidan:
```
1. Asosiy menyuda "ℹ️ Biz haqimizda" ni bosing
2. Kompaniya haqida ma'lumot ko'ring
3. Aksiyalar va afzalliklarni o'qing
4. Asosiy menyu avtomatik qaytadi
```

### 2. Har Xil Tillarda:
```
O'zbek:  ℹ️ Biz haqimizda
Rus:     ℹ️ О нас
Ingliz:  ℹ️ About Us
```

---

## 📊 Tarkibiy Qismlar

### 1. **Localization (bot/localization.py)**
Yangi tarjimalar qo'shildi:
```python
"btn_about_us": {
    "uz": "ℹ️ Biz haqimizda",
    "ru": "ℹ️ О нас",
    "en": "ℹ️ About Us"
}

"about_us_title": {...}
"about_us_info": {...}
```

### 2. **Klaviatura (bot/keyboards/reply.py)**
2 ustunli klaviatura:
```python
keyboard=[
    [btn1, btn2],  # 1-qator: 2 ta
    [btn3, btn4],  # 2-qator: 2 ta
    [btn5, btn6],  # 3-qator: 2 ta
]
```

### 3. **Handler (bot/handlers/start.py)**
Yangi handler:
```python
@router.message(F.text.in_([
    "ℹ️ Biz haqimizda", 
    "ℹ️ О нас", 
    "ℹ️ About Us"
]))
async def about_us(message: Message):
    # Ma'lumotlarni ko'rsatish
```

---

## ✏️ Ma'lumotlarni O'zgartirish

### "Biz haqimizda" Matnini Tahrirlash:

**Fayl:** `bot/localization.py`

**Joylashuv:** `TRANSLATIONS["about_us_info"]`

**Qanday o'zgartirish:**
```python
"about_us_info": {
    "uz": """
<b>OKS Suv</b> — sizning matn...

📍 <b>Manzil:</b>
Yangi manzil

📞 <b>Telefon:</b>
+998 XX XXX XX XX

🎉 <b>JORIY AKSIYALAR:</b>

🔥 Yangi aksiya:
   Sizning taklifingiz...
"""
}
```

**HTML Formatda:**
- `<b>Qalin</b>` - Bold matn
- `<i>Qiyshiq</i>` - Italic matn
- `<u>Tagiga chizilgan</u>` - Underline
- `<code>Kod</code>` - Monospace font

---

## 🎯 Foydalanish Senariylari

### Senariy 1: Kompaniya Ma'lumotlarini Ko'rish
```
Foydalanuvchi: "Telefon raqamingiz nima?"
→ ℹ️ Biz haqimizda → Telefon ko'radi
```

### Senariy 2: Aksiyalarni Bilish
```
Foydalanuvchi: "Qanday aksiyalar bor?"
→ ℹ️ Biz haqimizda → Aksiyalar ro'yxati
```

### Senariy 3: Ish Vaqtini Aniqlash
```
Foydalanuvchi: "Qachon buyurtma bera olaman?"
→ ℹ️ Biz haqimizda → Ish vaqti 08:00-22:00
```

---

## 💡 Tavsiyalar

### Aksiyalarni Yangilash:
Haftalik yoki oylik yangi aksiyalar qo'shing:
```python
🔥 <b>Dekabr aksiyasi:</b>
   Barcha buyurtmalarga 15% chegirma!
```

### Aloqa Ma'lumotlarini Saqlash:
Real telefon raqam va manzilni kiriting:
```python
📞 <b>Telefon:</b>
+998 XX XXX XX XX

📍 <b>Manzil:</b>
Termiz sh., Ko'cha nomi, Bino 00
```

### Ijtimoiy Tarmoqlar:
Ijtimoiy tarmoq havolalarini qo'shing:
```python
📱 <b>Ijtimoiy tarmoqlar:</b>
Telegram: @oks_suv
Instagram: @oks_suv
Facebook: facebook.com/okssuv
```

---

## 🧪 Test Qilish

### 1. Tugmani Test Qilish:
```
1. Botga /start yuboring
2. "ℹ️ Biz haqimizda" ni bosing
3. Ma'lumotlar to'g'ri chiqyaptimi?
4. Klaviatura qaytadimi?
```

### 2. Tillarni Test Qilish:
```
1. Tilni o'zgartiring (🌐)
2. "ℹ️ О нас" ni bosing (rus tilda)
3. Matn rus tilida chiqyaptimi?
4. Ingliz tilida ham tekshiring
```

### 3. Klaviaturani Test Qilish:
```
1. 6 ta tugma ko'rinmoqdami?
2. 2 ustunda joylashganmi? (3+3)
3. Barcha tugmalar ishlamoqdami?
```

---

## 📱 Mobil Qurilmalarda Ko'rinishi

### iPhone / Android:
```
┌─────────────────────────────────┐
│                                 │
│  🛒 Buyurtma    📋 Buyurtmalarim│
│     berish                      │
│                                 │
│  👤 Ma'lumot.   ℹ️ Biz haqimizda│
│                                 │
│  📞 Qo'llab-    🌐 Tilni        │
│     quvvatlash     o'zgartirish │
│                                 │
└─────────────────────────────────┘
```

**Qulay va zamonaviy!** ✨

---

## 🔧 Texnik Ma'lumotlar

### O'zgargan Fayllar:
1. ✅ `bot/localization.py` - Tarjimalar qo'shildi
2. ✅ `bot/keyboards/reply.py` - 2 ustunli klaviatura
3. ✅ `bot/handlers/start.py` - About Us handler

### Yangi Funksiyalar:
```python
# Handler
async def about_us(message: Message)

# Klaviatura
keyboard=[
    [btn1, btn2],  # 2 ustun
    [btn3, btn4],
    [btn5, btn6],
]
```

---

## ✅ Xulosa

### Qo'shildi:
- ✅ "ℹ️ Biz haqimizda" tugmasi
- ✅ 2 ustunli klaviatura (3+3)
- ✅ Kompaniya ma'lumotlari
- ✅ Aksiyalar ro'yxati
- ✅ 3 tilda qo'llab-quvvatlash

### Natija:
- ✨ Zamonaviy va ixcham dizayn
- ✨ Foydalanuvchilar uchun qulayroq
- ✨ Ko'proq ma'lumot bir joyda
- ✨ Aksiyalar va takliflar

---

**Yaratildi:** 05.07.2026, 18:45  
**Status:** ✅ Tayyor  
**Dasturchi:** Kiro AI Assistant

Yangi klaviatura va "Biz haqimizda" sahifasi tayyor! 🎉
