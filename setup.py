"""
JARVIS Setup Script
Automated setup for JARVIS AI Assistant
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} is not compatible")
        print("Please install Python 3.8 or higher")
        return False

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def test_microphone():
    """Test microphone access"""
    print("Testing microphone access...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
        print("✓ Microphone test successful")
        return True
    except Exception as e:
        print(f"✗ Microphone test failed: {e}")
        print("Please check your microphone permissions")
        return False

def test_tts():
    """Test text-to-speech"""
    print("Testing text-to-speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("JARVIS test successful")
        engine.runAndWait()
        print("✓ Text-to-speech test successful")
        return True
    except Exception as e:
        print(f"✗ Text-to-speech test failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["screenshots", "logs", "backups"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("JARVIS AI Assistant Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Create directories
    create_directories()
    
    # Test components
    print("\nTesting components...")
    test_microphone()
    test_tts()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nTo run JARVIS:")
    print("1. Voice mode: python jarvis_fixed.py")
    print("2. GUI mode: python jarvis_gui_simple.py")
    print("\nFor help, see README.md")
    
    return True

if __name__ == "__main__":
    main()
