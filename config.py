"""
JARVIS Configuration File
Advanced AI Assistant Configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_news_api_key_here')
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', 'your_email@gmail.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your_app_password')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_weather_api_key_here')
    
    # JARVIS Settings
    WAKE_WORD = os.getenv('WAKE_WORD', 'jarvis')
    VOICE_SPEED = int(os.getenv('VOICE_SPEED', '200'))
    VOICE_VOLUME = float(os.getenv('VOICE_VOLUME', '0.8'))
    CONTINUOUS_LISTENING = os.getenv('CONTINUOUS_LISTENING', 'true').lower() == 'true'
    SECURITY_LEVEL = os.getenv('SECURITY_LEVEL', 'high')
    AUTO_UPDATE = os.getenv('AUTO_UPDATE', 'true').lower() == 'true'
    LEARNING_MODE = os.getenv('LEARNING_MODE', 'enabled')
    
    # System Paths
    CHROME_PATH = os.getenv('CHROME_PATH', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
    SCREENSHOT_PATH = os.getenv('SCREENSHOT_PATH', './screenshots/')
    MUSIC_PATH = os.getenv('MUSIC_PATH', 'D:\\Music\\')
    DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', os.path.expanduser('~/Documents/'))
    
    # Advanced Features
    ENABLE_AI_CHAT = True
    ENABLE_SMART_HOME = True
    ENABLE_CALENDAR = True
    ENABLE_FILE_MANAGEMENT = True
    ENABLE_WEB_SCRAPING = True
    ENABLE_EMERGENCY_MODE = True
    
    # Security Settings
    FACE_RECOGNITION_THRESHOLD = 85
    VOICE_RECOGNITION_THRESHOLD = 80
    MAX_FAILED_ATTEMPTS = 3
    
    # AI Model Settings
    AI_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 150
    TEMPERATURE = 0.7
    
    # Notification Settings
    ENABLE_NOTIFICATIONS = True
    NOTIFICATION_SOUND = True
    DESKTOP_NOTIFICATIONS = True
