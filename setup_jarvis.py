"""
JARVIS Enhanced Setup Script
Complete setup and configuration for the enhanced JARVIS system
"""

import os
import sys
import subprocess
import json
from pathlib import Path

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

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = [
        "screenshots",
        "backups",
        "logs",
        "models",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_config_files():
    """Create configuration files"""
    print("Creating configuration files...")
    
    # Create .env file template
    env_template = """# JARVIS Configuration
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
WEATHER_API_KEY=your_weather_api_key_here

# JARVIS Settings
WAKE_WORD=jarvis
VOICE_SPEED=200
VOICE_VOLUME=0.8
CONTINUOUS_LISTENING=true
SECURITY_LEVEL=high
AUTO_UPDATE=true
LEARNING_MODE=enabled

# System Paths
CHROME_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
SCREENSHOT_PATH=./screenshots/
MUSIC_PATH=D:\\Music\\
DOCUMENTS_PATH=C:\\Users\\%USERNAME%\\Documents\\
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    
    # Create user preferences template
    user_preferences = {
        "name": "Sir",
        "preferred_voice": "male",
        "interests": [],
        "schedule": {},
        "security_level": "high",
        "voice_speed": 200,
        "voice_volume": 0.8,
        "common_commands": [],
        "time_patterns": {},
        "dislikes": []
    }
    
    with open('user_preferences.json', 'w') as f:
        json.dump(user_preferences, f, indent=2)
    
    # Create emergency contacts template
    emergency_contacts = {
        "police": "911",
        "fire": "911",
        "medical": "911",
        "family": [],
        "friends": [],
        "work": []
    }
    
    with open('emergency_contacts.json', 'w') as f:
        json.dump(emergency_contacts, f, indent=2)
    
    # Create automation rules template
    automation_rules = {
        "system_maintenance": {
            "daily_cleanup": True,
            "security_scan": True,
            "backup_files": True
        },
        "smart_scheduling": {
            "morning_routine": True,
            "evening_routine": True,
            "work_hours": "09:00-17:00"
        }
    }
    
    with open('automation_rules.json', 'w') as f:
        json.dump(automation_rules, f, indent=2)
    
    print("✓ Configuration files created")

def setup_face_recognition():
    """Setup face recognition system"""
    print("Setting up face recognition...")
    
    # Check if face recognition files exist
    face_recognition_path = Path("Face-Recognition")
    if face_recognition_path.exists():
        print("✓ Face recognition files found")
        
        # Check for trainer file
        trainer_path = face_recognition_path / "trainer" / "trainer.yml"
        if trainer_path.exists():
            print("✓ Face recognition trainer found")
        else:
            print("⚠ Face recognition trainer not found. Run Model Trainer.py to train the system")
    else:
        print("⚠ Face recognition directory not found")

def setup_chrome_driver():
    """Setup Chrome driver for web automation"""
    print("Setting up Chrome driver...")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        ChromeDriverManager().install()
        print("✓ Chrome driver setup complete")
    except Exception as e:
        print(f"⚠ Chrome driver setup failed: {e}")

def create_startup_scripts():
    """Create startup scripts"""
    print("Creating startup scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting JARVIS Enhanced System...
python jarvis_enhanced.py gui
pause
"""
    
    with open('start_jarvis.bat', 'w') as f:
        f.write(windows_script)
    
    # Linux/Mac shell script
    unix_script = """#!/bin/bash
echo "Starting JARVIS Enhanced System..."
python3 jarvis_enhanced.py gui
"""
    
    with open('start_jarvis.sh', 'w') as f:
        f.write(unix_script)
    
    # Make shell script executable
    try:
        os.chmod('start_jarvis.sh', 0o755)
    except:
        pass
    
    print("✓ Startup scripts created")

def run_system_check():
    """Run system compatibility check"""
    print("Running system check...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✓ Python version {python_version.major}.{python_version.minor} is compatible")
    else:
        print(f"⚠ Python version {python_version.major}.{python_version.minor} may have compatibility issues")
    
    # Check required modules
    required_modules = [
        'cv2', 'numpy', 'pyttsx3', 'speech_recognition', 
        'requests', 'psutil', 'pyautogui', 'schedule'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} is available")
        except ImportError:
            missing_modules.append(module)
            print(f"✗ {module} is missing")
    
    if missing_modules:
        print(f"Missing modules: {', '.join(missing_modules)}")
        return False
    
    return True

def create_documentation():
    """Create documentation files"""
    print("Creating documentation...")
    
    readme_content = """# JARVIS Enhanced - Iron Man Style AI Assistant

## Features

### 🤖 Advanced AI Capabilities
- OpenAI GPT integration for intelligent conversations
- Machine learning for user preferences
- Adaptive responses based on interaction history

### 🎤 Enhanced Voice System
- Wake word detection ("Jarvis")
- Continuous listening mode
- Voice authentication
- Multiple voice profiles (JARVIS, FRIDAY)

### 🛡️ Security & Emergency
- Multi-factor authentication (face + voice)
- Emergency protocols for medical, fire, security situations
- Real-time system monitoring
- Security event logging

### 🏠 Smart Automation
- System control (shutdown, restart, sleep, lock)
- File management and organization
- Task scheduling and reminders
- Smart home integration ready

### 📊 Advanced Features
- Calendar integration
- Email automation
- Web scraping capabilities
- Stock monitoring
- News aggregation

### 🖥️ Modern Interface
- Holographic-style GUI
- Real-time conversation log
- System status monitoring
- Voice control integration

## Installation

1. Run the setup script:
   ```bash
   python setup_jarvis.py
   ```

2. Configure your API keys in `.env` file:
   - OpenAI API key for AI features
   - News API key for news updates
   - Email credentials for email features
   - Weather API key for weather updates

3. Train face recognition (optional):
   ```bash
   python Face-Recognition/Model\ Trainer.py
   ```

## Usage

### GUI Mode (Recommended)
```bash
python jarvis_enhanced.py gui
```

### Voice Mode
```bash
python jarvis_enhanced.py voice
```

### Continuous Listening Mode
```bash
python jarvis_enhanced.py continuous
```

## Commands

### System Control
- "Jarvis, shutdown the system"
- "Jarvis, restart the computer"
- "Jarvis, lock the screen"
- "Jarvis, put the system to sleep"

### File Management
- "Jarvis, organize my desktop"
- "Jarvis, cleanup temporary files"
- "Jarvis, backup important files"
- "Jarvis, find file [filename]"

### Web & Information
- "Jarvis, search for [query]"
- "Jarvis, what's the news"
- "Jarvis, what's the weather"
- "Jarvis, search YouTube for [query]"

### Productivity
- "Jarvis, schedule a meeting"
- "Jarvis, send email to [person]"
- "Jarvis, remind me to [task]"
- "Jarvis, what's on my calendar"

### Emergency
- "Jarvis, emergency medical"
- "Jarvis, emergency fire"
- "Jarvis, emergency security"
- "Jarvis, call 911"

## Configuration

Edit `config.py` to customize:
- Voice settings
- Security levels
- Automation rules
- System paths

## Troubleshooting

### Voice Recognition Issues
- Ensure microphone is working
- Check speech recognition language settings
- Adjust energy threshold in `enhanced_voice.py`

### Face Recognition Issues
- Train the system with `Model Trainer.py`
- Ensure good lighting conditions
- Check camera permissions

### API Issues
- Verify API keys in `.env` file
- Check internet connection
- Review API usage limits

## Support

For issues and feature requests, please check the documentation or create an issue in the repository.

## License

This project is licensed under the MIT License.
"""
    
    with open('README_ENHANCED.md', 'w') as f:
        f.write(readme_content)
    
    print("✓ Documentation created")

def main():
    """Main setup function"""
    print("=" * 60)
    print("JARVIS Enhanced Setup")
    print("Iron Man Style AI Assistant")
    print("=" * 60)
    
    # Run system check
    if not run_system_check():
        print("System check failed. Please install missing dependencies.")
        return False
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements. Please check your internet connection.")
        return False
    
    # Create directories
    create_directories()
    
    # Create configuration files
    create_config_files()
    
    # Setup face recognition
    setup_face_recognition()
    
    # Setup Chrome driver
    setup_chrome_driver()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Create documentation
    create_documentation()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Copy .env.template to .env and add your API keys")
    print("2. Train face recognition (optional): python Face-Recognition/Model\\ Trainer.py")
    print("3. Start JARVIS: python jarvis_enhanced.py gui")
    print("\nFor help, see README_ENHANCED.md")
    
    return True

if __name__ == "__main__":
    main()
