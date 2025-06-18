# GetBandish Android APK Builder for Google Colab
# Instructions:
# 1. Go to https://colab.research.google.com
# 2. Create a new notebook
# 3. Copy and paste this entire script
# 4. Run all cells
# 5. Download your APK when it's ready!

print("GetBandish Android APK Builder")
print("=" * 40)

# Install buildozer and dependencies
print("Installing dependencies...")
!apt update -qq
!apt install -y python3-pip git zip unzip openjdk-8-jdk wget autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake
!pip install --upgrade buildozer cython

# Install Android SDK and NDK
print("Setting up Android SDK...")
!wget -q https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip
!unzip -q commandlinetools-linux-8512546_latest.zip
!mkdir -p /root/.buildozer/android/platform/android-sdk/cmdline-tools
!mv cmdline-tools /root/.buildozer/android/platform/android-sdk/cmdline-tools/latest

# Set environment variables
import os
os.environ['ANDROID_HOME'] = '/root/.buildozer/android/platform/android-sdk'
os.environ['ANDROID_SDK_ROOT'] = '/root/.buildozer/android/platform/android-sdk'
os.environ['PATH'] = os.environ['PATH'] + ':/root/.buildozer/android/platform/android-sdk/cmdline-tools/latest/bin'

print("Creating app files...")

# Create requirements.txt
with open('requirements.txt', 'w') as f:
    f.write("""kivy==2.2.0
kivymd==1.1.1""")

# NOTE: You need to copy your actual file contents here
# For now, I'll create placeholder files - you must replace these with your actual content

# Create main.py - REPLACE THIS WITH YOUR ACTUAL main.py CONTENT
print("IMPORTANT: You need to replace the file contents below with your actual app files!")
print("Copy your main.py, database.py, and data.py content into this script")

with open('main.py', 'w') as f:
    f.write('''# PLACEHOLDER - REPLACE WITH YOUR ACTUAL main.py CONTENT
# Copy the entire content from your main.py file here
print("This is a placeholder. Replace with your actual main.py content!")
''')

with open('database.py', 'w') as f:
    f.write('''# PLACEHOLDER - REPLACE WITH YOUR ACTUAL database.py CONTENT  
# Copy the entire content from your database.py file here
print("This is a placeholder. Replace with your actual database.py content!")
''')

with open('data.py', 'w') as f:
    f.write('''# PLACEHOLDER - REPLACE WITH YOUR ACTUAL data.py CONTENT
# Copy the entire content from your data.py file here
print("This is a placeholder. Replace with your actual data.py content!")
''')

# Create buildozer.spec with your updated configuration
with open('buildozer.spec', 'w') as f:
    f.write('''[app]
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

# Architecture
android.archs = arm64-v8a, armeabi-v7a

# Python for Android bootstrap
p4a.bootstrap = sdl2

[buildozer]
# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
''')

print("🔨 Building APK...")
print("⏰ This will take 10-20 minutes for the first build...")

# Build APK
!buildozer android debug

print("📥 Preparing APK for download...")

# Check if APK was created and download it
import os
if os.path.exists('bin/getbandish-1.0-debug.apk'):
    print("✅ APK built successfully!")
    print("📲 Downloading APK...")
    from google.colab import files
    files.download('bin/getbandish-1.0-debug.apk')
    print("🎉 Done! Install the APK on your Android device.")
else:
    print("❌ APK build failed. Check the logs above for errors.")
    print("📁 Available files in bin/:")
    !ls -la bin/ || echo "No bin directory found" 