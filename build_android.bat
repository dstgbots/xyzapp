@echo off
echo GetBandish Android Builder
echo ========================
echo.

echo Step 1: Installing dependencies...
py -m pip install --upgrade pip
py -m pip install kivy kivymd buildozer

echo.
echo Step 2: Building APK (this may take 10-15 minutes)...
py -c "import buildozer; print('Buildozer ready!')"
buildozer android debug

echo.
echo Step 3: APK created in bin folder!
echo You can now install it on your Android device.
echo.
pause 