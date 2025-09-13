"""
Enhanced Voice System for JARVIS
Advanced voice recognition and text-to-speech capabilities
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import queue
import keyboard
from config import Config
import numpy as np
from scipy.io import wavfile
import os

class EnhancedVoiceSystem:
    def __init__(self):
        self.config = Config()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # Configure TTS engine
        self.setup_tts()
        
        # Voice recognition settings
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
        # Wake word detection
        self.wake_word = self.config.WAKE_WORD.lower()
        self.is_listening = False
        self.is_awake = False
        
        # Audio queue for continuous listening
        self.audio_queue = queue.Queue()
        
        # Voice profiles
        self.voice_profiles = {
            "jarvis_male": 0,
            "jarvis_female": 1,
            "friday": 1
        }
        
    def setup_tts(self):
        """Setup text-to-speech engine with enhanced voices"""
        voices = self.engine.getProperty('voices')
        
        # Set voice properties
        self.engine.setProperty('rate', self.config.VOICE_SPEED)
        self.engine.setProperty('volume', self.config.VOICE_VOLUME)
        
        # Try to find the best voice
        for voice in voices:
            if 'english' in voice.name.lower() and 'male' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text, voice_type="jarvis_male"):
        """Enhanced speak function with voice selection"""
        try:
            # Set voice based on type
            voices = self.engine.getProperty('voices')
            if voice_type in self.voice_profiles:
                voice_id = self.voice_profiles[voice_type]
                if voice_id < len(voices):
                    self.engine.setProperty('voice', voices[voice_id].id)
            
            # Add JARVIS-style speaking patterns
            if not text.startswith(("Yes", "No", "I", "Sir", "Of course")):
                text = f"Yes Sir, {text}"
            
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    # Check for wake word
                    if self.wake_word in text:
                        self.is_awake = True
                        self.speak("Yes Sir, I'm listening")
                        return text
                        
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Wake word detection error: {e}")
                time.sleep(1)
    
    def listen_for_command(self, timeout=10):
        """Listen for user command after wake word"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"Command recognized: {command}")
                return command.lower()
            except sr.UnknownValueError:
                self.speak("I didn't catch that, Sir. Could you repeat?")
                return None
            except sr.RequestError as e:
                self.speak("I'm having trouble understanding you, Sir")
                return None
                
        except sr.WaitTimeoutError:
            self.speak("I'm waiting for your command, Sir")
            return None
    
    def continuous_listening(self):
        """Continuous listening mode"""
        self.is_listening = True
        self.speak("Continuous listening mode activated, Sir")
        
        while self.is_listening:
            try:
                command = self.listen_for_wake_word()
                if command:
                    # Process the command
                    yield command
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Continuous listening error: {e}")
                time.sleep(1)
    
    def voice_authentication(self):
        """Voice biometric authentication"""
        self.speak("Voice authentication required, Sir. Please say your passphrase")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            voice_text = self.recognizer.recognize_google(audio).lower()
            
            # Simple voice authentication (can be enhanced with voice recognition models)
            if "jarvis access" in voice_text or "tony stark" in voice_text:
                self.speak("Voice authentication successful, Sir")
                return True
            else:
                self.speak("Voice authentication failed")
                return False
                
        except Exception as e:
            self.speak("Authentication error occurred")
            return False
    
    def emergency_voice_activation(self):
        """Emergency voice activation system"""
        self.speak("Emergency protocols activated. What assistance do you require?")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            emergency_command = self.recognizer.recognize_google(audio).lower()
            return emergency_command
            
        except Exception as e:
            self.speak("Emergency command not recognized")
            return None
    
    def voice_feedback(self, success=True, message=""):
        """Provide voice feedback for actions"""
        if success:
            feedback_messages = [
                "Task completed successfully, Sir",
                "Done, Sir",
                "Mission accomplished",
                "All systems operational",
                "Task executed flawlessly"
            ]
            message = message or np.random.choice(feedback_messages)
        else:
            feedback_messages = [
                "I apologize, Sir. There was an issue",
                "Unable to complete task, Sir",
                "System error encountered",
                "Task failed, Sir"
            ]
            message = message or np.random.choice(feedback_messages)
        
        self.speak(message)
    
    def voice_notification(self, title, message):
        """Voice notifications for important events"""
        self.speak(f"Notification: {title}. {message}")
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        self.is_awake = False
        self.speak("Standing by, Sir")
