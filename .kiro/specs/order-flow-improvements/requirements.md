# Requirements Document

## Introduction

Ushbu hujjat OKS Suv Telegram botining buyurtma berish oqimini takomillashtirishga qaratilgan talablarni belgilaydi. Mavjud bot (Python + aiogram, SQLAlchemy) hozirda faqat bitta mahsulot (19 litrlik suv) sotadi va har bir buyurtmada foydalanuvchidan lokatsiya so'raydi.

Yangi funksionallik quyidagilarni o'z ichiga oladi:

- Ro'yxatdan o'tish oqimi o'zgarishsiz saqlanadi (ism → telefon → xonadondagi kishilar soni → tasdiq).
- Asosiy menyu tugmalari o'zgarishsiz saqlanadi.
- Buyurtma berishda bir nechta mahsulot ko'rsatiladi va har bir mahsulot yonida **+** va **−** tugmalari orqali son tanlash imkoniyati bo'ladi.
- Lokatsiya faqat birinchi marta so'raladi va mijoz profiliga saqlanadi; keyingi buyurtmalarda qayta so'ralmaydi.
- "Mening ma'lumotlarim" bo'limida saqlangan manzilni o'zgartirish imkoniyati bo'ladi.
- Buyurtma tasdiqlanadi va kanalga yuboriladi.

Bu hujjatdagi barcha talablar mavjud kodbaza tuzilishiga (users/orders jadvallari, lokalizatsiya tizimi, kanalga yuborish xizmati) mos ravishda yozilgan.

## Glossary

- **Bot**: OKS Suv Telegram boti (aiogram asosidagi tizim).
- **Registration_Service**: Yangi foydalanuvchini ro'yxatdan o'tkazuvchi komponent (`handlers/start.py`).
- **Order_Service**: Buyurtma yaratish oqimini boshqaruvchi komponent (`handlers/orders.py`).
- **Product_Catalog**: Sotuvdagi mahsulotlar ro'yxatini saqlovchi va taqdim etuvchi komponent.
- **Profile_Service**: Foydalanuvchi ma'lumotlarini (ism, telefon, xonadon, saqlangan manzil/lokatsiya) boshqaruvchi komponent.
- **Channel_Service**: Tasdiqlangan buyurtmani buyurtma kanaliga yuboruvchi komponent (`services/channel.py`).
- **Product**: Sotuvdagi bitta mahsulot birligi (nomi, narxi bilan). Masalan: "19 litr — 15 000 so'm".
- **Order_Item**: Bitta buyurtma ichidagi bitta mahsulot va uning tanlangan soni.
- **Order**: Bir yoki bir nechta Order_Item'dan iborat mijoz buyurtmasi.
- **Saved_Location**: Foydalanuvchi profiliga saqlangan manzil matni va (mavjud bo'lsa) geografik koordinatalar (kenglik/uzunlik).
- **Quantity_Selector**: Har bir mahsulot yonida ko'rsatiladigan son va **+** / **−** tugmalaridan iborat inline boshqaruv elementi.
- **Active_Order**: Holati "pending" (yetkazilmagan) bo'lgan buyurtma.

## Requirements

### Requirement 1: Ro'yxatdan o'tish oqimini saqlash

**User Story:** Yangi foydalanuvchi sifatida, men botni ishga tushirganimda ism, telefon va xonadondagi kishilar sonini kiritib ro'yxatdan o'tishni xohlayman, shunda men xizmatdan foydalana olaman.

#### Acceptance Criteria

1. WHEN foydalanuvchi `/start` buyrug'ini yuboradi AND foydalanuvchi ro'yxatdan o'tmagan, THE Registration_Service SHALL foydalanuvchidan to'liq ismini kiritishni so'raydi.
2. WHEN foydalanuvchi to'liq ismini kiritadi AND ism 3 dan 100 belgigacha bo'lsa, THE Registration_Service SHALL foydalanuvchidan telefon raqamini so'raydi.
3. WHEN foydalanuvchi telefon raqamini yuboradi AND raqam "+" bilan boshlanadi AND kamida 10 belgidan iborat AND "+" dan keyin faqat raqamlardan iborat, THE Registration_Service SHALL foydalanuvchidan xonadonda yashovchi kishilar sonini so'raydi.
4. WHEN foydalanuvchi xonadondagi kishilar sonini 1 dan 30 gacha bo'lgan butun son sifatida kiritadi, THE Registration_Service SHALL foydalanuvchi ma'lumotlarini (ism, telefon, kishilar soni) saqlaydi AND muvaffaqiyatli ro'yxatdan o'tganligi haqida tasdiq xabarini ko'rsatadi AND asosiy menyuni ko'rsatadi.
5. WHEN foydalanuvchi `/start` buyrug'ini yuboradi AND foydalanuvchi allaqachon ro'yxatdan o'tgan, THE Registration_Service SHALL asosiy menyuni ko'rsatadi AND ro'yxatdan o'tishni qayta so'ramaydi.
6. IF foydalanuvchi kiritgan ism 3 belgidan qisqa yoki 100 belgidan uzun, THEN THE Registration_Service SHALL xatolik xabarini ko'rsatadi AND ismni qayta so'raydi.
7. IF foydalanuvchi yuborgan telefon raqami "+" bilan boshlanmasa YOKI 10 belgidan qisqa bo'lsa YOKI "+" dan keyin raqam bo'lmagan belgi bo'lsa, THEN THE Registration_Service SHALL xatolik xabarini ko'rsatadi AND telefon raqamini qayta so'raydi.
8. IF foydalanuvchi kiritgan xonadondagi kishilar soni 1 dan 30 gacha bo'lgan butun son emas, THEN THE Registration_Service SHALL xatolik xabarini ko'rsatadi AND avval kiritilgan ma'lumotlarni saqlab qolgan holda sonni qayta so'raydi.

### Requirement 2: Asosiy menyu tugmalarini saqlash

**User Story:** Foydalanuvchi sifatida, men mavjud asosiy menyu tugmalarining o'zgarmasligini xohlayman, shunda menga tanish interfeys bilan ishlash oson bo'ladi.

#### Acceptance Criteria

1. WHILE foydalanuvchi ro'yxatdan o'tgan AND asosiy menyuda, THE Bot SHALL 6 ta tugmani 3 qator × 2 ustun tartibida ko'rsatadi: 1-qator (Buyurtma berish, Mening buyurtmalarim), 2-qator (Mening ma'lumotlarim, Biz haqimizda), 3-qator (Qo'llab-quvvatlash, Tilni o'zgartirish).
2. THE Bot SHALL asosiy menyu tugmalarining joriy joylashuvi (qator va ustun tartibi) va funksiyalarini o'zgartirmasdan saqlaydi.
3. WHEN foydalanuvchi biror amalni (buyurtma, ma'lumot ko'rish va h.k.) yakunlaydi, THE Bot SHALL foydalanuvchini asosiy menyuga qaytaradi AND o'sha 6 tugmani qayta ko'rsatadi.
4. WHILE foydalanuvchi tilni o'zgartirgan, THE Bot SHALL tugma matnlarini tanlangan tilga tarjima qiladi AND tugmalarning joylashuvi va funksiyalarini o'zgartirmaydi.

### Requirement 3: Bir nechta mahsulotni ko'rsatish

**User Story:** Mijoz sifatida, men buyurtma berishda bir nechta mahsulotdan tanlashni xohlayman, shunda men faqat 19 litrlik suvdan tashqari boshqa mahsulotlarni ham buyurtma qila olaman.

#### Acceptance Criteria

1. WHEN foydalanuvchi "Buyurtma berish" tugmasini bosadi AND foydalanuvchida Active_Order mavjud emas, THE Order_Service SHALL Product_Catalog'dagi mavjud (faol) barcha mahsulotlarni ro'yxat ko'rinishida 3 soniya ichida ko'rsatadi.
2. THE Product_Catalog SHALL har bir Product uchun nomini (1 dan 100 belgigacha) va narxini (0.01 dan 999 999 999.00 so'mgacha) ta'minlaydi.
3. WHEN Order_Service mahsulotlar ro'yxatini ko'rsatadi, THE Order_Service SHALL har bir Product yonida Quantity_Selector'ni ko'rsatadi.
4. WHERE Product_Catalog'da bir nechta mahsulot mavjud, THE Order_Service SHALL barcha mahsulotlarni bir xil formatda (nomi, narxi va Quantity_Selector tartibida) ko'rsatadi.
5. IF foydalanuvchida Active_Order mavjud, THEN THE Order_Service SHALL yangi buyurtma boshlamaydi AND aktiv buyurtma mavjudligini bildiruvchi ogohlantirish xabarini ko'rsatadi.
6. IF Product_Catalog'da birorta ham mavjud (faol) mahsulot bo'lmasa, THEN THE Order_Service SHALL yangi buyurtma boshlamaydi AND mahsulotlar mavjud emasligini bildiruvchi xabarni ko'rsatadi.
7. IF Product_Catalog'dan mahsulotlar ro'yxatini olish muvaffaqiyatsiz tugasa, THEN THE Order_Service SHALL buyurtma jarayonini boshlamaydi AND xatolik yuz berganini bildiruvchi xabarni ko'rsatadi AND foydalanuvchining oldingi holatini saqlaydi.

### Requirement 4: Mahsulot sonini + va − tugmalari orqali tanlash

**User Story:** Mijoz sifatida, men har bir mahsulot sonini + va − tugmalari orqali sozlashni xohlayman, shunda men har bir mahsulotdan kerakli miqdorni buyurtma qila olaman.

#### Acceptance Criteria

1. WHEN mahsulotlar ro'yxati foydalanuvchiga ko'rsatiladi, THE Quantity_Selector SHALL har bir Product uchun joriy tanlangan sonni butun raqam (0 dan 99 gacha) ko'rinishida ko'rsatadi.
2. WHEN foydalanuvchi biror Product yonidagi **+** tugmasini bosadi AND o'sha Product tanlangan soni 99 dan kichik, THE Order_Service SHALL o'sha Product tanlangan sonini 1 taga oshiradi AND yangilangan sonni 2 soniya ichida ko'rsatadi.
3. IF foydalanuvchi biror Product yonidagi **+** tugmasini bosadi AND o'sha Product tanlangan soni maksimal qiymatga (99) teng, THEN THE Order_Service SHALL sonni 99 da saqlaydi AND uni 99 dan yuqoriga oshirmaydi AND joriy sonni o'zgarishsiz ko'rsatadi.
4. WHEN foydalanuvchi biror Product yonidagi **−** tugmasini bosadi AND o'sha Product tanlangan soni 0 dan katta, THE Order_Service SHALL o'sha Product tanlangan sonini 1 taga kamaytiradi AND yangilangan sonni 2 soniya ichida ko'rsatadi.
5. IF foydalanuvchi biror Product yonidagi **−** tugmasini bosadi AND o'sha Product tanlangan soni minimal qiymatga (0) teng, THEN THE Order_Service SHALL sonni 0 da saqlaydi AND uni 0 dan pastga tushirmaydi AND joriy sonni o'zgarishsiz ko'rsatadi.
6. THE Order_Service SHALL har bir Product tanlangan sonining boshlang'ich qiymatini 0 deb belgilaydi.
7. THE Order_Service SHALL har bir Product uchun tanlangan sonni boshqa Productlarning tanlangan sonidan mustaqil ravishda saqlaydi va o'zgartiradi.

### Requirement 5: Buyurtmani yakunlash uchun kamida bitta mahsulot talab qilish

**User Story:** Mijoz sifatida, men bo'sh buyurtma bermasligim uchun tizim kamida bitta mahsulot tanlanganligini tekshirishini xohlayman.

#### Acceptance Criteria

1. WHEN foydalanuvchi mahsulot tanlashni yakunlash uchun davom etadi AND kamida bitta Product soni 1 dan katta yoki teng (1 dan 99 gacha oralig'ida), THE Order_Service SHALL 2 soniya ichida keyingi bosqichga (lokatsiya yoki tasdiqlash) o'tadi.
2. IF foydalanuvchi mahsulot tanlashni yakunlashga urinadi AND barcha Product'lar soni 0 ga teng, THEN THE Order_Service SHALL keyingi bosqichga o'tmaydi AND joriy bosqichda qoladi AND kamida bitta mahsulot tanlash kerakligini bildiruvchi xabarni 2 soniya ichida ko'rsatadi.
3. IF foydalanuvchi mahsulot tanlashni yakunlashga urinadi AND barcha Product'lar soni 0 ga teng, THEN THE Order_Service SHALL avval tanlangan mahsulot sonlari holatini o'zgarishsiz saqlab qoladi.
4. WHEN Order_Service buyurtmani yaratadi, THE Order_Service SHALL faqat soni 1 dan katta yoki teng bo'lgan har bir Product uchun bittadan Order_Item yaratadi AND soni 0 ga teng mahsulotlarni buyurtmaga kiritmaydi.

### Requirement 6: Buyurtma umumiy summasini hisoblash

**User Story:** Mijoz sifatida, men tanlangan mahsulotlarning umumiy summasini ko'rishni xohlayman, shunda men to'lovni oldindan bilaman.

#### Acceptance Criteria

1. WHEN buyurtmada kamida bitta Order_Item mavjud bo'ladi, THE Order_Service SHALL har bir Order_Item uchun oraliq summani (Product narxi × tanlangan son) hisoblaydi.
2. THE Order_Service SHALL barcha Order_Item oraliq summalari yig'indisi sifatida buyurtmaning umumiy summasini (0 dan 999 999 999 so'mgacha, butun songa yaxlitlangan) hisoblaydi.
3. WHEN tasdiqlash oynasi ko'rsatiladi, THE Order_Service SHALL har bir tanlangan mahsulot nomini, sonini, oraliq summasini va buyurtmaning umumiy summasini ko'rsatadi.
4. IF biror Order_Item soni 1 dan 99 gacha bo'lgan oraliqdan tashqarida bo'lsa, THEN THE Order_Service SHALL hisoblashni rad etadi AND xatolik xabarini ko'rsatadi AND tanlangan holatni saqlab qoladi.
5. IF biror Product narxi mavjud emas yoki manfiy bo'lsa, THEN THE Order_Service SHALL umumiy summani hisoblashni to'xtatadi AND xatolik yuz berganini bildiruvchi xabarni ko'rsatadi.

### Requirement 7: Birinchi buyurtmada lokatsiyani so'rash va saqlash

**User Story:** Mijoz sifatida, men lokatsiyamni faqat bir marta kiritishni xohlayman, shunda u profilimga saqlanadi va men uni har safar takrorlashim shart emas.

#### Acceptance Criteria

1. WHEN foydalanuvchi mahsulot tanlashni yakunlaydi AND foydalanuvchining Saved_Location'i mavjud emas, THE Order_Service SHALL foydalanuvchidan lokatsiya (koordinatalar) yoki manzil matnini kiritishni so'raydi.
2. WHEN foydalanuvchi mahsulot tanlashni yakunlaydi AND foydalanuvchining Saved_Location'i mavjud, THE Order_Service SHALL saqlangan lokatsiya va manzilni Order'ga avtomatik biriktiradi AND lokatsiyani qayta so'ramaydi.
3. WHEN foydalanuvchi lokatsiyani (koordinatalar) yuboradi, THE Order_Service SHALL koordinatalarni Order'ga biriktiradi AND foydalanuvchidan aniq manzil matnini so'raydi.
4. WHEN foydalanuvchi manzil matnini kiritadi AND matn kamida 5 belgidan va ko'pi bilan 200 belgidan iborat, THE Profile_Service SHALL manzil matnini va (mavjud bo'lsa) koordinatalarni foydalanuvchining Saved_Location'i sifatida saqlaydi.
5. IF foydalanuvchi kiritgan manzil matni 5 belgidan qisqa yoki 200 belgidan uzun, THEN THE Order_Service SHALL to'g'ri uzunlik talabini (5 dan 200 belgigacha) bildiruvchi xatolik xabarini ko'rsatadi AND avval kiritilgan koordinatalarni saqlab qolgan holda manzilni qayta so'raydi.
6. IF Saved_Location'ni saqlash amali muvaffaqiyatsiz tugaydi, THEN THE Profile_Service SHALL saqlash amalga oshmaganini bildiruvchi xatolik xabarini ko'rsatadi AND buyurtma jarayonini uzmasdan foydalanuvchidan qayta urinishni so'raydi.

### Requirement 8: Keyingi buyurtmalarda saqlangan lokatsiyani qayta ishlatish

**User Story:** Mijoz sifatida, men keyingi buyurtmalarimda lokatsiya so'ralmasligini xohlayman, shunda buyurtma berish tezroq bo'ladi.

#### Acceptance Criteria

1. WHEN foydalanuvchi mahsulot sonini kiritishni yakunlaydi AND foydalanuvchining Saved_Location'i to'liq (kamida 5 belgidan iborat manzil matni AND latitude/longitude koordinatalari mavjud), THE Order_Service SHALL lokatsiya va manzil so'rash bosqichlarini o'tkazib yuboradi AND to'g'ridan-to'g'ri tasdiqlash bosqichiga o'tadi.
2. WHEN Saved_Location to'liq bo'lgan buyurtma yaratiladi, THE Order_Service SHALL Saved_Location'dagi manzil matnini AND latitude/longitude koordinatalarini yangi Order'ga o'zgartirishsiz biriktiradi.
3. WHEN tasdiqlash oynasi ko'rsatiladi AND Saved_Location to'liq, THE Order_Service SHALL saqlangan manzil matnini buyurtma tarkibida ko'rsatadi.
4. IF foydalanuvchining Saved_Location'i mavjud emas OR to'liq emas (manzil matni 5 belgidan kam OR koordinatalar yo'q), THEN THE Order_Service SHALL lokatsiya so'rash bosqichini ko'rsatadi AND tasdiqlash bosqichiga faqat manzil va koordinatalar kiritilgandan so'ng o'tadi.

### Requirement 9: Saqlangan manzilni "Mening ma'lumotlarim" bo'limida o'zgartirish

**User Story:** Mijoz sifatida, men "Mening ma'lumotlarim" bo'limida saqlangan manzilimni o'zgartirishni xohlayman, shunda men ko'chib o'tganimda yoki xato kiritganimda uni yangilay olaman.

#### Acceptance Criteria

1. WHEN foydalanuvchi "Mening ma'lumotlarim" bo'limini ochadi, THE Profile_Service SHALL foydalanuvchining ismi, telefoni, xonadondagi kishilar soni va joriy Saved_Location'ini ko'rsatadi.
2. THE Profile_Service SHALL "Mening ma'lumotlarim" bo'limida manzilni o'zgartirish uchun tugma ko'rsatadi.
3. WHEN foydalanuvchi manzilni o'zgartirish tugmasini bosadi, THE Profile_Service SHALL foydalanuvchidan GPS lokatsiya yoki matnli manzil kiritishni so'raydi.
4. WHEN foydalanuvchi GPS lokatsiya yuboradi yoki matnli manzil (5 dan 200 belgigacha, bo'sh joylar olib tashlangandan keyin) kiritadi, THE Profile_Service SHALL Saved_Location'ni yangi qiymat bilan almashtiradi.
5. WHEN Profile_Service Saved_Location'ni muvaffaqiyatli yangilaydi, THE Profile_Service SHALL yangi manzil qiymatini aks ettiruvchi tasdiq xabarini ko'rsatadi.
6. IF foydalanuvchi kiritgan yangi manzil matni 5 belgidan qisqa yoki 200 belgidan uzun, THEN THE Profile_Service SHALL manzil uzunligi talabini bildiruvchi xatolik xabarini ko'rsatadi AND joriy Saved_Location'ni o'zgartirmasdan saqlab qoladi AND manzilni qayta so'raydi.
7. IF Saved_Location'ni saqlash amaliyoti muvaffaqiyatsiz tugasa, THEN THE Profile_Service SHALL amaliyot bajarilmaganligini bildiruvchi xatolik xabarini ko'rsatadi AND avvalgi Saved_Location'ni o'zgartirmasdan saqlab qoladi.

### Requirement 10: Buyurtmani tasdiqlash

**User Story:** Mijoz sifatida, men buyurtmani yuborishdan oldin tekshirib tasdiqlashni xohlayman, shunda men xato buyurtma bermasligimga ishonch hosil qilaman.

#### Acceptance Criteria

1. WHEN foydalanuvchi buyurtma tafsilotlarini kiritishni yakunlaydi va yetkazib berish manzili mavjud bo'ladi, THE Order_Service SHALL har bir tanlangan mahsulot nomi, har bir mahsulot soni, har bir mahsulot bo'yicha oraliq summa, umumiy summa va yetkazib berish manzilini o'z ichiga olgan tasdiqlash oynasini ko'rsatadi.
2. THE Order_Service SHALL tasdiqlash oynasida "Tasdiqlash" va "Bekor qilish" tugmalarini ko'rsatadi.
3. IF tasdiqlash oynasini ko'rsatish so'ralganda savatda birorta ham mahsulot bo'lmasa (mahsulotlar soni 0 ga teng), THEN THE Order_Service SHALL tasdiqlash oynasini ko'rsatmaydi AND savat bo'shligini bildiruvchi xabarni ko'rsatadi AND foydalanuvchini asosiy menyuga qaytaradi.
4. WHEN foydalanuvchi "Tasdiqlash" tugmasini bosadi, THE Order_Service SHALL buyurtmaga oldingi eng katta buyurtma raqamidan bittaga katta bo'lgan noyob navbatdagi butun buyurtma raqamini beradi.
5. WHEN buyurtmaga raqam berilgan bo'ladi, THE Order_Service SHALL buyurtmani "pending" holatida saqlaydi.
6. WHEN buyurtma muvaffaqiyatli saqlanadi, THE Order_Service SHALL foydalanuvchiga buyurtma raqamini o'z ichiga olgan muvaffaqiyatli tasdiq xabarini ko'rsatadi AND foydalanuvchini asosiy menyuga qaytaradi.
7. IF buyurtmani saqlash amali muvaffaqiyatsiz tugasa, THEN THE Order_Service SHALL buyurtmani saqlamaydi (hech qanday qisman yozuv qoldirmaydi) AND foydalanuvchiga saqlash amalga oshmaganini bildiruvchi va qayta urinishni taklif qiluvchi xato xabarini ko'rsatadi AND kiritilgan buyurtma tafsilotlarini saqlab qoladi.
8. WHEN foydalanuvchi "Bekor qilish" tugmasini bosadi, THE Order_Service SHALL buyurtmani saqlamaydi AND foydalanuvchini asosiy menyuga qaytaradi.

### Requirement 11: Buyurtmani kanalga yuborish

**User Story:** Xizmat egasi sifatida, men tasdiqlangan buyurtmalarning barcha tafsilotlari bilan kanalga yuborilishini xohlayman, shunda yetkazib berish jarayonini boshqarishim mumkin.

#### Acceptance Criteria

1. WHEN buyurtma muvaffaqiyatli tasdiqlanadi AND buyurtma kanali sozlangan, THE Channel_Service SHALL buyurtma ma'lumotlarini 10 soniya ichida buyurtma kanaliga yuboradi.
2. THE Channel_Service SHALL kanal xabarida buyurtma raqamini, mijoz ismini, telefon raqamini, xonadon o'lchamini (kishilar soni), barcha tanlangan mahsulotlar va sonlarini, umumiy summani, yetkazib berish manzilini va buyurtma yaratilgan sana-vaqtni ko'rsatadi.
3. WHERE buyurtmaga koordinatalar (kenglik va uzunlik) biriktirilgan, THE Channel_Service SHALL kanalga lokatsiyani (xarita nuqtasi) ham yuboradi.
4. THE Channel_Service SHALL kanal xabariga "Yetkazildi" deb belgilash tugmasini va boshlang'ich "Yetkazilmoqda" holat belgisini biriktiradi.
5. WHEN kanal xabari muvaffaqiyatli yuboriladi, THE Channel_Service SHALL kanal xabari identifikatorini buyurtmaga saqlaydi.
6. IF buyurtma kanali sozlanmagan, THEN THE Channel_Service SHALL kanalga hech qanday xabar yubormaydi va buyurtma jarayonini uzmasdan davom ettiradi.
7. IF kanalga yuborish Telegram API xatosi tufayli muvaffaqiyatsiz bo'lsa, THEN THE Channel_Service SHALL yuborishni ko'pi bilan 3 marta qayta uradi, barcha urinishlar muvaffaqiyatsiz tugasa xatolikni qayd etadi va buyurtma ma'lumotlarini o'zgarishsiz saqlab qoladi.

### Requirement 12: "Mening buyurtmalarim" ro'yxatida bir nechta mahsulotni ko'rsatish

**User Story:** Mijoz sifatida, men o'tmishdagi buyurtmalarimda barcha buyurtma qilingan mahsulotlarni ko'rishni xohlayman, shunda men nima buyurtma qilganimni eslay olaman.

#### Acceptance Criteria

1. WHEN foydalanuvchi "Mening buyurtmalarim" bo'limini ochadi AND buyurtmalar mavjud, THE Order_Service SHALL eng so'nggi buyurtmalarni (ko'pi bilan 10 tasini) sana bo'yicha kamayish tartibida (eng yangisi birinchi) ko'rsatadi.
2. WHEN buyurtmalar ro'yxati ko'rsatiladi, THE Order_Service SHALL har bir buyurtma uchun buyurtma raqamini, barcha Order_Item'larni, umumiy summani, manzilni, sanani va yetkazib berish holatini ko'rsatadi.
3. WHEN buyurtma ko'rsatiladi, THE Order_Service SHALL har bir Order_Item'ni alohida (mahsulot nomi va soni bilan) ko'rsatadi.
4. IF foydalanuvchida buyurtmalar mavjud emas, THEN THE Order_Service SHALL buyurtmalar yo'qligi haqidagi xabarni ko'rsatadi.
5. IF buyurtmalar ro'yxatini olish muvaffaqiyatsiz tugasa, THEN THE Order_Service SHALL xatolik yuz berganini bildiruvchi xabarni ko'rsatadi AND foydalanuvchini asosiy menyuga qaytaradi.

### Requirement 13: Ko'p tillilikni saqlash

**User Story:** Foydalanuvchi sifatida, men yangi funksiyalar tanlagan tilimda ko'rsatilishini xohlayman, shunda men bot bilan qulay ishlay olaman.

#### Acceptance Criteria

1. THE Bot SHALL barcha yangi foydalanuvchiga yo'naltirilgan matnlarni (mahsulot ro'yxati, son tanlash, manzil so'rovi, buyurtmani tasdiqlash va buyurtmani o'zgartirish xabarlari) O'zbek (uz), Rus (ru) va Ingliz (en) tillarining har birida ta'minlaydi.
2. WHILE foydalanuvchi uch tildan (uz, ru, en) birini tanlagan holatda, THE Bot SHALL mahsulot ro'yxati, son tanlash, manzil so'rovi, buyurtmani tasdiqlash va buyurtmani o'zgartirish xabarlarini o'sha tilda ko'rsatadi.
3. WHEN foydalanuvchi buyurtma jarayonining istalgan qadamida tilni o'zgartiradi, THE Bot SHALL keyingi ko'rsatiladigan barcha foydalanuvchiga yo'naltirilgan matnlarni yangi tanlangan tilda ko'rsatadi va joriy buyurtma ma'lumotlarini saqlab qoladi.
4. IF foydalanuvchi hech qanday til tanlamagan yoki tanlangan til uch qo'llab-quvvatlanadigan til (uz, ru, en) ichida bo'lmasa, THEN THE Bot SHALL matnlarni O'zbek (uz) tilida ko'rsatadi.
5. IF tanlangan tilda biror foydalanuvchiga yo'naltirilgan matn mavjud bo'lmasa, THEN THE Bot SHALL o'sha matnni O'zbek (uz) tilidagi variantida ko'rsatadi va bo'sh yoki tarjimasiz xabar yubormaydi.
