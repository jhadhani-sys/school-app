# خطوات بديلة لبناء APK عندما يكون الاتصال بالإنترنت محدوداً

## المشكلة الحالية
البيئة الحالية مقيدة من ناحية الاتصال بالإنترنت (وجود proxy يرفع "403 Forbidden"). buildozer يحتاج لتحميل:
- Android SDK
- Android NDK
- python-for-android
- مكتبات أخرى

## الحلول البديلة

### 1. ✅ الحل الأفضل: استخدام GitHub Actions (موصى به)
```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build APK
        uses: ArtemSBulgakov/buildozer-action@master
        with:
          command: buildozer android debug
          workdir: school_management_android
      - name: Upload APK
        uses: actions/upload-artifact@v2
        with:
          name: apk
          path: school_management_android/bin/
```

انسخ هذا الملف إلى: `.github/workflows/build.yml`

### 2. استخدام Android Studio محلياً
1. ثبّت Android Studio من: https://developer.android.com/studio
2. افتح المشروع وأنشئ APK من Build > Make Project
3. سيتولى Android Studio تحميل كل الأدوات المطلوبة

### 3. استخدام نسخة Buildozer عبر الإنترنت
إذا كان لديك وصول إنترنت عادي (بدون proxy)، يمكنك:
```bash
cd school_management_android
buildozer android debug
```

### 4. استخدام Docker على جهاز آخر
```bash
docker run -it --rm \
  -v $(pwd)/school_management_android:/home/user/host \
  kivy/buildozer buildozer android debug
```

## ملاحظات مهمة
- الحل الأول (GitHub Actions) هو الأسهل والأكثر موثوقية
- APK سيكون جاهزاً في `bin/` بعد الانتهاء من البناء
- اسم الملف: `schoolmanagement-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`

## التثبيت على جهاز Android
```bash
# بعد الحصول على ملف APK
adb install bin/schoolmanagement-1.0.0-arm64-v8a_armeabi-v7a-debug.apk

# أو انقل الملف يدوياً إلى الجهاز والضغط عليه
```

## حل سريع إضافي: استخدام نسخة بدون اتصال
إذا أردت بناء APK بدون الاتصال بالإنترنت بشكل كامل:
1. استخدم نسخة مُعدة مسبقاً من SDK/NDK
2. أو استخدم buildozer مع `--private` flag

```bash
buildozer android debug -- --private $HOME/.buildozer/android/platform/android-sdk
```
