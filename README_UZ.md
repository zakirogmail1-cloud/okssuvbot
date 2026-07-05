# 💧 OKS Suv Bot - Readme

## 📋 Umumiy Ma'lumot

**Bot Nomi:** OKS Suv  
**Maqsad:** Termiz shahrida ichimlik suvi yetkazib berish xizmati  
**Telegram Bot:** [@oks_suv_bot](https://t.me/your_bot_username)  
**Versiya:** 2.0  
**Oxirgi Yangilanish:** 05.07.2026

---

## ✨ Asosiy Imkoniyatlar

### 👥 Foydalanuvchilar Uchun:
- 📝 Ro'yxatdan o'tish (ism, telefon, xonadon hajmi)
- 🛒 Suv buyurtma berish
- 📍 Lokatsiya yuborish yoki manzil yozish
- 📋 Buyurtmalar tarixini ko'rish
- ✏️ Shaxsiy ma'lumotlarni o'zgartirish
- 📞 Qo'llab-quvvatlash xizmati
- 💧 Kunlik eslatmalar (avtomatik)

### 👨‍💼 Adminlar Uchun:
- 📊 Kunlik hisobotlar (Excel, PDF)
- 📊 Haftalik hisobotlar
- 📊 Oylik hisobotlar
- 👥 Barcha mijozlar ro'yxati
- 📱 Kanal orqali buyurtmalarni boshqarish
- ✅ Buyurtmani yetkazildi deb belgilash

---

## 🚀 Ishga Tushirish

### 1. Talablar:
```
Python 3.9+
PostgreSQL (Supabase)
Telegram Bot Token
```

### 2. O'rnatish:
```bash
# Reponi klonlash
cd "c:\Users\abdul\OneDrive\Desktop\oks bot\oks_suv_bot"

# Virtual environment yaratish
python -m venv venv
venv\Scripts\activate

# Paketlarni o'rnatish
pip install -r requirements.txt
```

### 3. Konfiguratsiya:
`.env` faylini yarating:
```env
BOT_TOKEN=sizning_bot_tokeningiz
ADMIN_TELEGRAM_IDS=admin_id1,admin_id2
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
DAILY_CHANNEL_ID=-1001234567890
```

### 4. Ishga tushirish:
```bash
python -m bot.main
```

---

## 📁 Loyiha Strukturasi

```
oks_suv_bot/
├── bot/
│   ├── handlers/          # Buyruqlar va xabarlarni boshqarish
│   │   ├── start.py       # /start, ro'yxatdan o'tish
│   │   ├── orders.py      # Buyurtmalar
│   │   └── admin.py       # Admin paneli
│   ├── keyboards/         # Klaviatura tugmalari
│   │   ├── reply.py       # Reply keyboards
│   │   └── inline.py      # Inline keyboards
│   ├── database/          # Database
│   │   ├── models.py      # SQLAlchemy modellari
│   │   ├── crud.py        # CRUD operatsiyalari
│   │   └── connection.py  # Database ulanishi
│   ├── services/          # Xizmatlar
│   │   ├── scheduler.py   # APScheduler
│   │   ├── notifications.py # Eslatmalar
│   │   └── channel.py     # Kanal boshqaruvi
│   ├── middlewares/       # Middleware'lar
│   │   └── throttling.py  # Rate limiting
│   ├── utils/             # Yordamchi funksiyalar
│   │   └── stickers.py    # Sticker yuborish
│   ├── config.py          # Konfiguratsiya
│   └── main.py            # Asosiy fayl
├── web/                   # Web panel (FastAPI)
│   ├── app.py
│   └── templates/
├── requirements.txt       # Python paketlar
└── .env                   # Environment o'zgaruvchilar
```

---

## 🗄️ Database Strukturasi

### Users (Foydalanuvchilar):
```sql
- id (int, PK)
- telegram_id (bigint, unique)
- full_name (varchar)
- phone (varchar)
- household_size (int)
- created_at (datetime)
- last_reminder_at (datetime, nullable)
```

### Orders (Buyurtmalar):
```sql
- id (int, PK)
- order_number (int)
- user_id (int, FK)
- quantity (int)
- address (text)
- location_lat (float, nullable)
- location_lng (float, nullable)
- status (enum: pending, delivered)
- channel_message_id (int, nullable)
- created_at (datetime)
```

### Admins (Adminlar):
```sql
- id (int, PK)
- telegram_id (bigint, unique)
- full_name (varchar)
```

---

## ⚙️ Asosiy Funksiyalar

### 1. Ro'yxatdan O'tish
```python
/start → Ism → Telefon → Xonadon hajmi → ✅
```

### 2. Buyurtma Berish
```python
🛒 Buyurtma berish → 
  Mahsulot tanlash → 
  Soni kiritish → 
  Manzil/Lokatsiya → 
  Tasdiqlash → ✅
```

### 3. Kunlik Eslatmalar
```python
Har kuni soat 10:00 da:
- Xonadon hajmiga qarab interval
- 4 kishi → 7 kun
- 5 kishi → 5 kun
- 6 kishi → 4 kun
- 7+ kishi → 3 kun
```

### 4. Admin Hisobotlar
```python
/admin → 
  📊 Kunlik/Haftalik/Oylik →
  Excel va PDF formatda yuklab olish
```

---

## 🔧 Sozlamalar

### Timezone:
```python
UZBEKISTAN_TZ = UTC+5
Barcha vaqtlar O'zbekiston vaqti bilan
```

### Rate Limiting:
```python
30 so'rov / 60 sekund
Anti-spam himoya
```

### Scheduler:
```python
APScheduler (AsyncIO)
Kunlik eslatmalar: 10:00
```

---

## ✅ Tuzatilgan Xatolar

### 05.07.2026 - Versiya 2.0:
1. ✅ Timezone xatosi (UTC → UTC+5)
2. ✅ Import xatolari (ReplyKeyboardRemove)
3. ✅ Type hinting (Python 3.9 uyg'unligi)
4. ✅ Klaviatura muammosi (buyurtmadan keyin)

Batafsil: `XATOLAR_TUZATILDI.md`

---

## 📞 Qo'llab-quvvatlash

### Foydalanuvchilar uchun:
- Bot ichida: 📞 Qo'llab-quvvatlash
- Xabar adminlarga avtomatik yuboriladi

### Dasturchilar uchun:
- Issues: GitHub Issues
- Email: support@okssuv.uz
- Telegram: @admin_username

---

## 📊 Statistika

Bot quyidagilarni kuzatadi:
- ✅ Jami foydalanuvchilar
- ✅ Kunlik buyurtmalar
- ✅ Yetkazilgan buyurtmalar
- ✅ Aktiv foydalanuvchilar

---

## 🔐 Xavfsizlik

### Amalga oshirilgan:
- ✅ Environment variables (.env)
- ✅ Admin tekshiruvi
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection himoya (SQLAlchemy)

### Tavsiyalar:
- 🔒 Bot tokenni hech qayerga ko'rsatmang
- 🔒 Database parolni himoya qiling
- 🔒 Admin ID larni .env da saqlang
- 🔒 HTTPS ishlatilsin (production)

---

## 🚀 Production Deploy

### Variantlar:
1. **Railway** - Tavsiya etiladi
2. **Heroku** - Oddiy deploy
3. **VPS** - To'liq nazorat
4. **Docker** - Konteynerlashtirish

### Railway uchun:
```bash
# railway.json mavjud
railway up
```

---

## 📝 Litsenziya

MIT License - Erkin foydalaning!

---

## 🙏 Minnatdorchilik

- Aiogram - Telegram Bot framework
- SQLAlchemy - ORM
- FastAPI - Web framework
- APScheduler - Task scheduler
- Supabase - PostgreSQL hosting

---

## 📅 Roadmap

### Kelgusida qo'shilishi rejalashtirilgan:
- [ ] Payment integratsiyasi (Click, Payme)
- [ ] Multi-language (O'zbek, Rus)
- [ ] Bonus tizimi
- [ ] Referal dastur
- [ ] Mobil ilovaga API
- [ ] Geo-tracking (yetkazuvchi joylashuvi)
- [ ] SMS xabarnoma
- [ ] Web admin panel

---

## 🎉 Versiya Tarixi

### v2.0 (05.07.2026)
- ✅ Barcha xatolar tuzatildi
- ✅ Klaviatura muammosi hal qilindi
- ✅ Timezone to'g'rilandi
- ✅ Code clean-up

### v1.0 (29.06.2026)
- ✅ Asosiy funksiyalar
- ✅ Database migration
- ✅ Admin panel
- ✅ Kanal integratsiyasi

---

**Ishlab chiqildi:** OKS Team  
**Tuzatuvchi:** Kiro AI Assistant  
**Sana:** 05.07.2026

**Bot tayyor va ishlamoqda!** 🎉💧
