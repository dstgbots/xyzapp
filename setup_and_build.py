#!/usr/bin/env python3
"""
Setup and build script for GetBandish Android app
Run this script to build and install the app on your Android device
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in {description}:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("GetBandish Android App Builder")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("Error: main.py not found. Please run this script from the project directory.")
        return
    
    print("\n📱 Building Android APK...")
    print("This may take several minutes for first build...")
    
    # Install dependencies first
    if not run_command("py -m pip install kivy kivymd buildozer", "Installing dependencies"):
        print("Failed to install dependencies. Please install Python and pip properly.")
        return
    
    # Initialize buildozer (first time only)
    if not os.path.exists("buildozer.spec"):
        run_command("buildozer init", "Initializing buildozer")
    
    # Build APK
    if run_command("buildozer android debug", "Building APK"):
        print("\n🎉 APK built successfully!")
        
        # Check if ADB is available for direct installation
        try:
            subprocess.run("adb version", shell=True, check=True, capture_output=True)
            
            print("\n📲 Installing on connected Android device...")
            apk_path = "bin/getbandish-1.0-debug.apk"
            
            if os.path.exists(apk_path):
                if run_command(f"adb install -r {apk_path}", "Installing APK on device"):
                    print("\n✅ App installed successfully on your device!")
                    print("Look for 'GetBandish' app in your app drawer.")
                else:
                    print(f"\n📁 APK created at: {apk_path}")
                    print("You can manually install it on your phone.")
            else:
                print("\nAPK file not found. Check the bin/ directory.")
                
        except subprocess.CalledProcessError:
            print("\n⚠️ ADB not found. You'll need to install the APK manually.")
            print("The APK file is located in the 'bin' folder.")
    
    else:
        print("\n❌ Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 