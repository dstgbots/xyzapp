# GetBandish Android APK Build Guide

## 🎯 Quick Start - 3 Ways to Build Your APK

### 📱 Option 1: Google Colab (Recommended)

**Why Colab?** Free, no setup needed, works on any device!

1. Go to: https://colab.research.google.com
2. Create a new notebook
3. Copy the entire content from `colab_build.py`
4. **IMPORTANT**: Replace these placeholder sections with your actual file content:

```python
# Replace this section:
with open('main.py', 'w') as f:
    f.write('''# PLACEHOLDER - REPLACE WITH YOUR ACTUAL main.py CONTENT''')

# With your actual main.py content:
with open('main.py', 'w') as f:
    f.write('''
# Copy and paste your entire main.py file content here
# All 3800+ lines of code
''')
```

5. Do the same for `database.py` and `data.py`
6. Run all cells (takes 10-15 minutes)
7. Download your APK!

### 🐧 Option 2: Linux Virtual Machine

If you have access to Linux or WSL:

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-8-jdk
pip3 install buildozer

# In your project directory
buildozer android debug

# APK will be in bin/ folder
```

### ☁️ Option 3: Online Build Services

1. **Buildbot.io** - Upload your project and build online
2. **GitHub Actions** - Set up automated building
3. **Replit** - Import project and build there

## 📋 Pre-Build Checklist

✅ All Python files are included (main.py, database.py, data.py)
✅ buildozer.spec is properly configured
✅ requirements.txt lists all dependencies
✅ No absolute file paths in your code
✅ Database file will be created automatically on first run

## 🔧 Buildozer Configuration

Your `buildozer.spec` is already configured with:

- **Package**: org.kousthubh.getbandish
- **Permissions**: Internet, Storage
- **API Level**: 31
- **Requirements**: Python3, Kivy 2.2.0, KivyMD 1.1.1
- **Architecture**: ARM64 + ARMv7

## 📱 Testing Your APK

1. **Enable Developer Options** on your Android device
2. **Allow Unknown Sources** in security settings
3. **Install** the APK file
4. **Launch** GetBandish app
5. **Test** all features:
   - Browse raagas and bandish
   - Create concerts
   - Add custom bandish
   - Search functionality

## 🐛 Common Issues & Solutions

### "App crashes on startup"
- Check if database.py and data.py are included
- Verify all import statements work

### "Custom bandish not saving"
- Ensure storage permissions are granted
- Check if app has write access

### "Build fails in Colab"
- Make sure you replaced ALL placeholder content
- Check that file content is properly escaped

### "APK is too large"
- Remove unused imports
- Compress any image assets
- Use only required KivyMD components

## 📊 APK Details

- **Size**: ~15-25 MB
- **Min Android**: 7.0 (API 24)
- **Target Android**: 12 (API 31)
- **Architecture**: Universal (ARM64 + ARMv7)
- **Permissions**: Internet, Storage

## 🚀 Distribution

Once your APK is ready:

1. **Test thoroughly** on different devices
2. **Consider Play Store** upload for wider distribution
3. **Share via Google Drive, Dropbox, or direct transfer**
4. **Create user guide** for installation

## 📝 Notes

- First build takes 15-20 minutes
- Subsequent builds are faster (5-10 minutes)
- APK works on Android 7.0+
- No internet required except for initial data
- Database is stored locally on device

## 🎉 Success!

Your GetBandish app will include:
- ✅ All raaga and bandish data
- ✅ Concert creation and management
- ✅ Custom bandish creation
- ✅ Search functionality
- ✅ Beautiful Material Design UI
- ✅ Offline functionality 