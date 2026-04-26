# خطة إنشاء تطبيق Android APK - نظام إدارة المدرسة

## الخطوات المنجزة

1. [x] فحص وفهم المشروع الحالي
2. [x] إنشاء `src/utils/helpers.py` - مسارات التخزين المتوافقة مع Android
3. [x] تحديث `src/modules/license.py` - إصلاح توليد معرف الجهاز والمسارات
4. [x] تحديث `src/modules/auth.py` - المسارات الديناميكية
5. [x] تحديث `src/database/db_manager.py` - المسارات الديناميكية
6. [x] إعادة كتابة `main.py` - إصلاح بنية الشاشات والحوارات وزر الرجوع
7. [x] تحديث `buildozer.spec` - الإعدادات الصحيحة للبناء
8. [x] تحديث `requirements.txt` - إزالة المكتبات المدمجة
9. [x] اختبار syntax والتأكد من عدم وجود أخطاء

## التعديلات الرئيسية

### 1. إصلاح بنية الشاشات
- تحويل `StudentsScreen`، `TeachersScreen`، `GradesScreen`، `ReportsScreen`، `SettingsScreen` من `MDScreen` إلى `MDBoxLayout` عادي
- هذا يمنع تعارض `ScreenManager` مع `MDBottomNavigation` ويحل مشكلة العرض على Android

### 2. إصلاح إدارة الحوارات (Dialogs)
- إضافة `self.dialog = None` بعد كل `dismiss()`
- استخدام `nonlocal self` في دوال callback الداخلية
- منع الاستدعاءات القديمة المتوقفة (stale callbacks)

### 3. مسارات التخزين المتوافقة مع Android
- إنشاء `StorageHelper` للحصول على مسار التخزين المناسب للمنصة
- استخدام `app.user_data_dir` على Android
- تخزين قاعدة البيانات وملفات الترخيص في المسار الصحيح

### 4. معالجة زر الرجوع في Android
- إضافة `Window.bind(on_keyboard=self.on_keyboard)`
- زر الرجوع يظهر حوار تأكيد الخروج من الشاشة الرئيسية
- يعود إلى شاشة الترخيص من شاشة تسجيل الدخول إن لم يكن مفعلاً

### 5. إصلاحات أخرى
- إزالة `sqlite3` من `requirements.txt` و `buildozer.spec` (مكتبة مدمجة في Python)
- إضافة `plyer` للحصول على معرف الجهاز على Android
- استخدام `%` formatting بدلاً من f-strings لتوافق أفضل مع Kivy

## خطوات بناء APK

### الطريقة 1: باستخدام Docker (الأسهل)
```bash
cd school_management_android
docker run -it --rm -v "$PWD":/home/user/host kivy/buildozer buildozer android debug
```

### الطريقة 2: باستخدام buildozer محلي
```bash
cd school_management_android
pip install buildozer
buildozer android debug
```

### ملاحظات
- أول بناء سيستغرق وقتًا طويلاً (30-60 دقيقة) لتحميل Android SDK/NDK
- ملف APK الناتج سيكون في `bin/schoolmanagement-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`
- للبناء السريع التالي: `buildozer android debug deploy run`
