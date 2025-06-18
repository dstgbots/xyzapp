[app]
# Application title
title = GetBandish

# Package name
package.name = getbandish

# Package domain
package.domain = org.kousthubh.getbandish

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,txt

# Version
version = 1.0

# Requirements
requirements = python3,kivy==2.2.0,kivymd==1.1.1,sqlite3

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android API level
android.api = 31

# Android NDK version
android.ndk = 25b

# Android SDK version
android.sdk = 31

# Orientation
orientation = portrait

# Icons and splash
#icon.filename = %(source.dir)s/icon.png
#presplash.filename = %(source.dir)s/presplash.png

# Architecture
android.archs = arm64-v8a, armeabi-v7a

# Android metadata
android.gradle_dependencies = 

# Python for Android bootstrap
p4a.bootstrap = sdl2

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2 