"""
JARVIS Fixed - Microphone Access Fixed
Fixed version with better microphone handling
"""

import pyttsx3
import wikipedia
import speech_recognition as sr
import webbrowser
import datetime
import os
import sys
import requests
import psutil
import pyjokes
import pyautogui
import cv2
import threading
import time
from helpers import *
from news import speak_news, getNewsUrl
from youtube import youtube

class FixedJARVIS:
    def __init__(self):
        # Initialize TTS engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 0.9)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Test microphone
        self.test_microphone()
        
        # Setup browser
        self.setup_browser()
        
        print("JARVIS Fixed System Initialized")
    
    def test_microphone(self):
        """Test microphone access"""
        try:
            print("Testing microphone access...")
            with self.microphone as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("Microphone test successful!")
        except Exception as e:
            print(f"Microphone test failed: {e}")
            print("Please check your microphone permissions and try again.")
    
    def setup_browser(self):
        """Setup web browser"""
        if sys.platform == "win32":
            chrome_paths = [
                'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    self.chrome_path = path
                    break
            else:
                self.chrome_path = None
        else:
            self.chrome_path = '/usr/bin/google-chrome'
        
        try:
            if self.chrome_path:
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))
        except:
            pass  # Use default browser if Chrome not found
    
    def speak(self, text):
        """Text to speech with error handling"""
        try:
            print(f"JARVIS: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
            print(f"JARVIS: {text}")
    
    def listen(self):
        """Listen for voice commands with better error handling"""
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                self.speak("I didn't catch that, Sir. Could you repeat?")
                return None
            except sr.RequestError as e:
                self.speak("I'm having trouble understanding you, Sir")
                print(f"Speech recognition error: {e}")
                return None
                
        except sr.WaitTimeoutError:
            self.speak("I'm waiting for your command, Sir")
            return None
        except Exception as e:
            self.speak("I encountered an error while listening, Sir")
            print(f"Listening error: {e}")
            return None
    
    def wish_me(self):
        """Greeting function"""
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            greeting = "Good Morning, Sir"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon, Sir"
        else:
            greeting = "Good Evening, Sir"
        
        self.speak(greeting)
        
        # Get weather
        try:
            weather()
        except Exception as e:
            print(f"Weather error: {e}")
        
        self.speak("I am JARVIS Fixed. How may I assist you today, Sir?")
    
    def execute_command(self, query):
        """Execute voice commands"""
        try:
            print(f"Executing command: {query}")
            
            # Wikipedia search
            if 'wikipedia' in query:
                self.speak('Searching Wikipedia....')
                query = query.replace('wikipedia', '')
                try:
                    results = wikipedia.summary(query, sentences=2)
                    self.speak('According to Wikipedia')
                    print(results)
                    self.speak(results)
                except Exception as e:
                    self.speak("Sorry, I couldn't find information on that topic")
                    print(f"Wikipedia error: {e}")
            
            # YouTube search
            elif 'search youtube' in query:
                self.speak('What you want to search on Youtube?')
                search_term = self.listen()
                if search_term:
                    try:
                        youtube(search_term)
                        self.speak(f"Searching YouTube for {search_term}")
                    except Exception as e:
                        self.speak("Sorry, I couldn't search YouTube")
                        print(f"YouTube error: {e}")
            
            # Open websites
            elif 'open youtube' in query:
                try:
                    webbrowser.open('https://youtube.com')
                    self.speak("Opening YouTube, Sir")
                except Exception as e:
                    self.speak("Sorry, I couldn't open YouTube")
                    print(f"Browser error: {e}")
            
            elif 'open google' in query:
                try:
                    webbrowser.open('https://google.com')
                    self.speak("Opening Google, Sir")
                except Exception as e:
                    self.speak("Sorry, I couldn't open Google")
                    print(f"Browser error: {e}")
            
            elif 'open amazon' in query:
                try:
                    webbrowser.open('https://amazon.com')
                    self.speak("Opening Amazon, Sir")
                except Exception as e:
                    self.speak("Sorry, I couldn't open Amazon")
                    print(f"Browser error: {e}")
            
            elif 'open stackoverflow' in query:
                try:
                    webbrowser.open('https://stackoverflow.com')
                    self.speak("Opening Stack Overflow, Sir")
                except Exception as e:
                    self.speak("Sorry, I couldn't open Stack Overflow")
                    print(f"Browser error: {e}")
            
            # System information
            elif 'cpu' in query:
                try:
                    cpu()
                except Exception as e:
                    self.speak("Sorry, I couldn't get CPU information")
                    print(f"CPU error: {e}")
            
            elif 'joke' in query:
                try:
                    joke()
                except Exception as e:
                    self.speak("Sorry, I couldn't tell a joke")
                    print(f"Joke error: {e}")
            
            elif 'screenshot' in query:
                self.speak("Taking screenshot")
                try:
                    screenshot()
                except Exception as e:
                    self.speak("Sorry, I couldn't take a screenshot")
                    print(f"Screenshot error: {e}")
            
            # Time
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f'Sir, the time is {strTime}')
            
            # Search
            elif 'search' in query:
                self.speak('What do you want to search for?')
                search_term = self.listen()
                if search_term:
                    try:
                        url = f'https://google.com/search?q={search_term}'
                        webbrowser.open(url)
                        self.speak(f'Here is what I found for {search_term}')
                    except Exception as e:
                        self.speak("Sorry, I couldn't perform the search")
                        print(f"Search error: {e}")
            
            # Location
            elif 'location' in query:
                self.speak('What is the location?')
                location = self.listen()
                if location:
                    try:
                        url = f'https://google.nl/maps/place/{location}/&amp;'
                        webbrowser.open(url)
                        self.speak(f'Here is the location {location}')
                    except Exception as e:
                        self.speak("Sorry, I couldn't find the location")
                        print(f"Location error: {e}")
            
            # News
            elif 'news' in query:
                self.speak('Of course sir..')
                try:
                    speak_news()
                    self.speak('Do you want to read the full news...')
                    test = self.listen()
                    if test and 'yes' in test:
                        self.speak('Ok Sir, Opening browser...')
                        webbrowser.open(getNewsUrl())
                        self.speak('You can now read the full news from this website.')
                    else:
                        self.speak('No Problem Sir')
                except Exception as e:
                    self.speak("Sorry, I couldn't get the news")
                    print(f"News error: {e}")
            
            # Voice change
            elif 'voice' in query:
                try:
                    voices = self.engine.getProperty('voices')
                    if voices and len(voices) > 1:
                        if 'female' in query:
                            self.engine.setProperty('voice', voices[1].id)
                        else:
                            self.engine.setProperty('voice', voices[0].id)
                        self.speak("Hello Sir, I have switched my voice. How is it?")
                    else:
                        self.speak("Sorry, I only have one voice available")
                except Exception as e:
                    self.speak("Sorry, I couldn't change my voice")
                    print(f"Voice change error: {e}")
            
            # System control
            elif 'shutdown' in query:
                self.speak("Shutting down system in 30 seconds, Sir")
                try:
                    os.system("shutdown /s /t 30")
                except Exception as e:
                    self.speak("Sorry, I couldn't shutdown the system")
                    print(f"Shutdown error: {e}")
            
            elif 'restart' in query:
                self.speak("Restarting system in 30 seconds, Sir")
                try:
                    os.system("shutdown /r /t 30")
                except Exception as e:
                    self.speak("Sorry, I couldn't restart the system")
                    print(f"Restart error: {e}")
            
            elif 'sleep' in query:
                self.speak("Putting system to sleep, Sir")
                try:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                except Exception as e:
                    self.speak("Sorry, I couldn't put the system to sleep")
                    print(f"Sleep error: {e}")
            
            elif 'lock' in query:
                self.speak("Locking system, Sir")
                try:
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                except Exception as e:
                    self.speak("Sorry, I couldn't lock the system")
                    print(f"Lock error: {e}")
            
            # Volume control
            elif 'volume up' in query:
                try:
                    pyautogui.press('volumeup')
                    self.speak("Volume increased, Sir")
                except Exception as e:
                    self.speak("Sorry, I couldn't increase the volume")
                    print(f"Volume error: {e}")
            
            elif 'volume down' in query:
                try:
                    pyautogui.press('volumedown')
                    self.speak("Volume decreased, Sir")
                except Exception as e:
                    self.speak("Sorry, I couldn't decrease the volume")
                    print(f"Volume error: {e}")
            
            elif 'mute' in query:
                try:
                    pyautogui.press('volumemute')
                    self.speak("Audio muted, Sir")
                except Exception as e:
                    self.speak("Sorry, I couldn't mute the audio")
                    print(f"Mute error: {e}")
            
            # JARVIS responses
            elif 'jarvis are you there' in query:
                self.speak("Yes Sir, at your service")
            
            elif 'jarvis who made you' in query:
                self.speak("Yes Sir, my master built me with AI")
            
            elif 'your name' in query:
                self.speak('My name is JARVIS')
            
            elif 'who made you' in query:
                self.speak('I was created by my AI master')
            
            elif 'stands for' in query:
                self.speak('J.A.R.V.I.S stands for JUST A RATHER VERY INTELLIGENT SYSTEM')
            
            elif 'your friend' in query:
                self.speak('My friends are Google assistant, Alexa and Siri')
            
            # File operations
            elif 'remember that' in query:
                self.speak("What should I remember sir")
                remember_message = self.listen()
                if remember_message:
                    self.speak(f"You said me to remember {remember_message}")
                    try:
                        with open('data.txt', 'w') as f:
                            f.write(remember_message)
                    except Exception as e:
                        self.speak("Sorry, I couldn't save that")
                        print(f"Save error: {e}")
            
            elif 'do you remember anything' in query:
                try:
                    with open('data.txt', 'r') as f:
                        content = f.read()
                    self.speak(f"You said me to remember that {content}")
                except:
                    self.speak("I don't remember anything, Sir")
            
            # Exit
            elif 'sleep' in query or 'goodbye' in query or 'exit' in query:
                self.speak("Goodbye Sir, have a great day!")
                return False
            
            else:
                self.speak("I didn't understand that command, Sir. Could you try again?")
            
            return True
            
        except Exception as e:
            self.speak(f"I apologize, Sir. An error occurred: {str(e)}")
            print(f"Command execution error: {e}")
            return True
    
    def run(self):
        """Main run function"""
        self.wish_me()
        
        while True:
            try:
                command = self.listen()
                if command:
                    if not self.execute_command(command):
                        break
            except KeyboardInterrupt:
                self.speak("Goodbye Sir!")
                break
            except Exception as e:
                print(f"Main loop error: {e}")
                self.speak("I encountered an error, Sir. Let's continue.")

def main():
    """Main function"""
    print("=" * 60)
    print("JARVIS Fixed - Microphone Access Fixed")
    print("=" * 60)
    
    jarvis = FixedJARVIS()
    jarvis.run()

if __name__ == "__main__":
    main()

