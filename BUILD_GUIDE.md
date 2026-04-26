# دليل بناء تطبيق Android APK - نظام إدارة المدرسة

## ✅ الحالة الحالية
تم إصلاح جميع أخطاء الكود والمشاكل المتعلقة بالبناء. التطبيق جاهز للبناء.

## 🔧 ما تم إصلاحه
1. **بنية الشاشات**: تحويل التبويبات من `MDScreen` إلى `MDBoxLayout` لتجنب تعارضات `ScreenManager`
2. **المسارات الديناميكية**: استخدام `StorageHelper` للحصول على مسارات التخزين الصحيحة على Android
3. **إدارة الحوارات**: إصلاح مشاكل `self.dialog` المتكرر وإضافة تنظيف صحيح
4. **زر الرجوع في Android**: إضافة معالجة زر الرجوع مع تأكيد الخروج
5. **buildozer.spec**: إزالة `reportlab` وإصلاح الإعدادات

## 🚀 طرق بناء APK

### الطريقة 1: GitHub Actions (الأسهل والأفضل)
لا تحتاج لأي إعدادات محلية. فقط ارفع الكود على GitHub.

**الخطوات:**
1. أنشئ مستودع GitHub جديد
2. ارفع محتوى مجلد `school_management_android` إلى المستودع
3. ادفع (push) الكود إلى فرع `main`
4. GitHub Actions سيبني APK تلقائياً
5. ستجد ملف APK في قسم **Actions** → **Artifacts**

ملف سير العمل موجود في: `.github/workflows/build.yml`

### الطريقة 2: Docker محلياً
إذا كان لديك Docker مثبت:

```bash
cd school_management_android
docker run -it --rm \
  -v $(pwd):/home/user/host \
  kivy/buildozer \
  buildozer android debug
```

### الطريقة 3: buildozer محلي
إذا كان لديك إنترنت بدون proxy:

```bash
cd school_management_android
pip install buildozer
buildozer android debug
```

## 📦 ملف الإخراج
بعد البناء بنجاح، ستجد ملف APK في:
```
school_management_android/bin/schoolmanagement-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

## 📱 تثبيت APK على الهاتف

### الطريقة 1: ADB
```bash
adb install bin/schoolmanagement-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

### الطريقة 2: يدوياً
1. انقل ملف APK إلى هاتفك
2. فعّل "تثبيت من مصادر غير معروفة" في الإعدادات
3. اضغط على ملف APK للتثبيت

## 🔑 بيانات الدخول الافتراضية
- **اسم المستخدم:** `admin`
- **كلمة المرور:** `admin123`

## 📝 ملاحظات هامة
- التطبيق يتطلب تفعيل ترخيص على كل جهاز (يُنشأ تلقائياً)
- البيانات تُخزن محلياً في قاعدة بيانات SQLite
- الصلاحيات المطلوبة: INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
