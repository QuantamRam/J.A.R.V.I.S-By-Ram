# JARVIS By Ram - AI Voice Assistant

<div align="center">
  <img src="jarvis1.jpg" alt="JARVIS AI Assistant" width="400"/>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](README.md)
  [![Voice Recognition](https://img.shields.io/badge/Voice%20Recognition-Google%20Speech-blue.svg)](https://cloud.google.com/speech-to-text)
</div>

## 🤖 Overview

JARVIS (Just A Rather Very Intelligent System) is an advanced AI voice assistant inspired by Tony Stark's JARVIS from the Iron Man movies. This intelligent assistant can perform various tasks through voice commands, including web searches, system control, file management, and much more.

## ✨ Features

### 🎤 Voice Commands
- **Voice Recognition**: Advanced speech-to-text using Google Speech Recognition
- **Text-to-Speech**: Natural voice responses with multiple voice options
- **Wake Word Detection**: Responds to "Jarvis" wake word
- **Continuous Listening**: Always-on voice recognition mode

### 🌐 Web Integration
- **Web Search**: Google search integration
- **YouTube Search**: Direct YouTube video searches
- **Website Navigation**: Open popular websites (Google, YouTube, Amazon, Stack Overflow)
- **News Updates**: Real-time news headlines
- **Weather Information**: Current weather data

### 💻 System Control
- **System Management**: Shutdown, restart, sleep, lock
- **Volume Control**: Adjust system volume
- **Screenshot**: Capture screen images
- **CPU Monitoring**: System performance monitoring
- **File Operations**: Remember and recall information

### 🎯 Smart Features
- **Wikipedia Integration**: Instant knowledge lookup
- **Joke Telling**: Entertainment with programming jokes
- **Location Services**: Map integration for location searches
- **Memory System**: Remember user preferences and information
- **Multi-language Support**: English voice recognition

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 or higher**
- **Windows 10/11** (Linux and macOS support available)
- **Microphone and speakers**
- **Internet connection**
- **Chrome browser** (optional, for web automation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run JARVIS**
   ```bash
   python jarvis_fixed.py
   ```

## 📋 Detailed Setup Instructions

### Step 1: Environment Setup

1. **Install Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Verify Python installation**
   ```bash
   python --version
   pip --version
   ```

### Step 2: Repository Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv jarvis_env
   
   # Windows
   jarvis_env\Scripts\activate
   
   # Linux/macOS
   source jarvis_env/bin/activate
   ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `pyttsx3` - Text-to-speech engine
- `SpeechRecognition` - Voice recognition
- `requests` - HTTP requests
- `wikipedia` - Wikipedia API
- `psutil` - System information
- `pyjokes` - Programming jokes
- `opencv-python` - Computer vision
- `pyautogui` - GUI automation

### Step 4: Microphone Setup

1. **Check microphone permissions**
   - Windows: Settings > Privacy > Microphone
   - Ensure microphone access is enabled for Python

2. **Test microphone**
   ```bash
   python -c "import speech_recognition as sr; print('Microphone test passed')"
   ```

### Step 5: Run JARVIS

```bash
python jarvis_fixed.py
```

## 🎯 Usage Examples

### Voice Commands

| Command | Description | Example |
|---------|-------------|---------|
| `"Jarvis, what's the time"` | Get current time | "Sir, the time is 14:30:25" |
| `"Jarvis, search for Python"` | Web search | Opens Google search |
| `"Jarvis, open YouTube"` | Open website | Opens YouTube |
| `"Jarvis, tell me a joke"` | Entertainment | Tells programming joke |
| `"Jarvis, what's the weather"` | Weather info | Current weather data |
| `"Jarvis, shutdown"` | System control | Shutdowns computer |
| `"Jarvis, wikipedia AI"` | Knowledge lookup | Wikipedia summary |

### Text Commands

You can also use the GUI version for text-based commands:

```bash
python jarvis_gui_simple.py
```

## 🔧 Configuration

### Voice Settings

Edit the voice parameters in `jarvis_fixed.py`:

```python
self.engine.setProperty('rate', 200)      # Speech rate (words per minute)
self.engine.setProperty('volume', 0.9)    # Volume level (0.0 to 1.0)
```

### Browser Settings

Configure browser paths in the `setup_browser()` method:

```python
chrome_paths = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
]
```

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working**
   ```bash
   # Check microphone permissions
   # Windows: Settings > Privacy > Microphone
   # Test with: python -c "import speech_recognition as sr; print('OK')"
   ```

2. **Speech recognition errors**
   ```bash
   # Check internet connection
   # Google Speech Recognition requires internet
   ```

3. **TTS not working**
   ```bash
   # Install additional TTS engines
   pip install pyttsx3[espeak]
   ```

4. **Browser not opening**
   ```bash
   # Check Chrome installation path
   # Update browser paths in setup_browser()
   ```

### Error Codes

| Error | Solution |
|-------|----------|
| `MicrophoneNotFound` | Check microphone connection |
| `RequestError` | Check internet connection |
| `UnknownValueError` | Speak more clearly |
| `PermissionError` | Run as administrator |

## 📁 Project Structure

```
jarvis-ai-assistant/
├── jarvis_fixed.py          # Main JARVIS application (fixed version)
├── jarvis_simple.py         # Simple JARVIS version
├── jarvis_gui_simple.py     # GUI version
├── jarvis_enhanced.py       # Enhanced version (advanced features)
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
├── helpers.py              # Helper functions
├── news.py                 # News functionality
├── youtube.py              # YouTube integration
├── OCR.py                  # Optical Character Recognition
├── diction.py              # Dictionary functionality
├── Face-Recognition/       # Face recognition system
│   ├── Face recognition.py
│   ├── Model Trainer.py
│   └── trainer/
├── images/                 # Image assets
└── data.json              # Dictionary data
```

## 🚀 Deployment to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `jarvis-ai-assistant` (or your preferred name)
3. Make it public or private as needed

### Step 2: Initialize Git

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: JARVIS AI Assistant"

# Add remote origin
git remote add origin https://github.com/yourusername/jarvis-ai-assistant.git

# Push to GitHub
git push -u origin main
```

### Step 3: Create .gitignore

Create a `.gitignore` file:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# JARVIS specific
data.txt
*.wav
*.mp3
screenshots/
logs/
```

### Step 4: Update Repository

```bash
# Add changes
git add .

# Commit changes
git commit -m "Update: Add new features"

# Push to GitHub
git push origin main
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Areas for Contribution

- Additional voice commands
- New integrations (APIs, services)
- UI/UX improvements
- Performance optimizations
- Documentation updates
- Bug fixes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google for Speech Recognition API
- Wikipedia for knowledge base
- The open-source community for various libraries
- Marvel Studios for the JARVIS inspiration

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/jarvis-ai-assistant/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/jarvis-ai-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jarvis-ai-assistant/discussions)

## 🔮 Roadmap

### Version 2.0 (Coming Soon)
- [ ] GUI interface improvements
- [ ] Additional voice commands
- [ ] Smart home integration
- [ ] Multi-language support
- [ ] Cloud synchronization

### Version 3.0 (Future)
- [ ] Advanced AI integration
- [ ] Mobile app companion
- [ ] Augmented reality interface
- [ ] Neural network optimization

---

<div align="center">
  <strong>Built with ❤️ for the future of AI assistants</strong>
  
  [⭐ Star this repo](https://github.com/yourusername/jarvis-ai-assistant) | 
  [🐛 Report Bug](https://github.com/yourusername/jarvis-ai-assistant/issues) | 
  [💡 Request Feature](https://github.com/yourusername/jarvis-ai-assistant/issues)
</div>
