# URY Mosaic Notification Tizimi

## Qo'shilgan xususiyatlar

### Toast Notification Komponenti

URY Mosaic desktop ilovasiga professional toast notification tizimi qo'shildi. Bu tizim ekranning o'ng tomonida paydo bo'ladigan xabarnomalar orqali foydalanuvchilarni turli hodisalar haqida xabardor qiladi.

### Notification Turlari

1. **Success (Muvaffaqiyatli)** - Yashil rang
   - Buyurtma tayyor bo'lganda
   - Buyurtma tasdiqlanganda
   - Internet ulanish tiklandiganda

2. **Error (Xato)** - Qizil rang
   - Xatolik yuz berganda
   - Internet ulanish uzilganda

3. **Warning (Ogohlantirish)** - Sariq rang
   - Buyurtma bekor qilingan

4. **Info (Ma'lumot)** - Ko'k rang
   - Yangi buyurtma kelganda
   - Buyurtma o'zgartirilganda

### Qayerlarda Ishlatiladi

#### 1. Serve (Tayyor) tugmasi bosilganda:
```
✓ Buyurtma tayyor bo'ldi!
```

#### 2. Confirm (Tasdiqlash) tugmasi bosilganda:
```
✓ Buyurtma tasdiqlandi!
```

#### 3. Yangi buyurtma kelganda:
```
🔔 Yangi buyurtma - [Stol raqami/Takeaway]
```

#### 4. Buyurtma o'zgartirilganda:
```
ℹ Buyurtma o'zgartirildi - [Stol raqami/Takeaway]
```

#### 5. Buyurtma bekor qilinganda:
```
⚠ Buyurtma bekor qilindi - [Stol raqami/Takeaway]
```

#### 6. Internet ulanishi:
```
✓ Internet ulanish tiklandi
✕ Internet ulanish uzildi
```

### Xususiyatlar

- **Avtomatik yo'qolish**: Notificationlar 5 soniyadan keyin avtomatik yo'qoladi
- **Yopish tugmasi**: Har bir notificationni qo'lda yopish mumkin
- **Animatsiya**: Notificationlar o'ng tomondan sirg'alib kiradi va chiqadi
- **Ko'p xabarnoma**: Bir vaqtning o'zida bir nechta notification ko'rsatilishi mumkin
- **Responsive**: Barcha ekran o'lchamlariga moslashadi

### Texnik ma'lumotlar

- **Framework**: Vue.js 3
- **Komponent**: `/URYMosaic/src/components/Toast.vue`
- **Foydalanilgan joy**: `/URYMosaic/src/components/kot.vue`
- **CSS**: Tailwind CSS bilan moslashtirilgan

### Ishga tushirish

1. Ilovani build qilish:
```bash
cd /home/sardorbek/frappe-bench/apps/ury_mosaic/URYMosaic
yarn build
```

2. Cache tozalash:
```bash
cd /home/sardorbek/frappe-bench
bench clear-cache
```

3. Brauzerda sahifani yangilash (Ctrl + F5)

### Kelajakdagi yaxshilanishlar

- Tovush bilan xabarnomalar
- Notification tarixini saqlash
- Custom xabarnomalar sozlamalari
- Notification o'lchami va joylashuvini sozlash imkoniyati
