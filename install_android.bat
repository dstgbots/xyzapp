@echo off
echo Installing GetBandish App on Android Device...
echo.
echo Make sure:
echo 1. Your phone is connected via USB
echo 2. USB Debugging is ON
echo 3. Developer Options are enabled
echo.
pause

echo Installing dependencies...
py -m pip install kivy kivymd buildozer

echo Building APK...
py -m buildozer android debug

echo.
echo Installing APK on device...
adb install -r bin\getbandish-1.0-debug.apk

echo.
echo Done! Check your phone for GetBandish app.
pause 