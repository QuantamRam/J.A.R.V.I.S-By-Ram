"""
JARVIS Simple - Core Working Features
Simplified version focusing on working features only
"""

import pyttsx3
import wikipedia
import speech_recognition as sr
import webbrowser
import datetime
import os
import sys
import smtplib
import requests
import psutil
import pyjokes
import pyautogui
import cv2
from helpers import *
from news import speak_news, getNewsUrl
from youtube import youtube

class SimpleJARVIS:
    def __init__(self):
        # Initialize TTS engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 200)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Setup browser
        self.setup_browser()
        
        print("JARVIS Simple System Initialized")
    
    def setup_browser(self):
        """Setup web browser"""
        if sys.platform == "win32":
            self.chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        else:
            self.chrome_path = '/usr/bin/google-chrome'
        
        try:
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))
        except:
            pass  # Use default browser if Chrome not found
    
    def speak(self, text):
        """Text to speech"""
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice commands"""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            command = self.recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("I didn't catch that, Sir. Could you repeat?")
            return None
        except sr.RequestError:
            self.speak("I'm having trouble understanding you, Sir")
            return None
        except sr.WaitTimeoutError:
            self.speak("I'm waiting for your command, Sir")
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
        except:
            pass
        
        self.speak("I am JARVIS Simple. How may I assist you today, Sir?")
    
    def execute_command(self, query):
        """Execute voice commands"""
        try:
            # Wikipedia search
            if 'wikipedia' in query:
                self.speak('Searching Wikipedia....')
                query = query.replace('wikipedia', '')
                results = wikipedia.summary(query, sentences=2)
                self.speak('According to Wikipedia')
                print(results)
                self.speak(results)
            
            # YouTube search
            elif 'search youtube' in query:
                self.speak('What you want to search on Youtube?')
                search_term = self.listen()
                if search_term:
                    youtube(search_term)
            
            # Open websites
            elif 'open youtube' in query:
                webbrowser.open('https://youtube.com')
                self.speak("Opening YouTube, Sir")
            
            elif 'open google' in query:
                webbrowser.open('https://google.com')
                self.speak("Opening Google, Sir")
            
            elif 'open amazon' in query:
                webbrowser.open('https://amazon.com')
                self.speak("Opening Amazon, Sir")
            
            elif 'open stackoverflow' in query:
                webbrowser.open('https://stackoverflow.com')
                self.speak("Opening Stack Overflow, Sir")
            
            # System information
            elif 'cpu' in query:
                cpu()
            
            elif 'joke' in query:
                joke()
            
            elif 'screenshot' in query:
                self.speak("Taking screenshot")
                screenshot()
            
            # Time
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f'Sir, the time is {strTime}')
            
            # Search
            elif 'search' in query:
                self.speak('What do you want to search for?')
                search_term = self.listen()
                if search_term:
                    url = f'https://google.com/search?q={search_term}'
                    webbrowser.open(url)
                    self.speak(f'Here is what I found for {search_term}')
            
            # Location
            elif 'location' in query:
                self.speak('What is the location?')
                location = self.listen()
                if location:
                    url = f'https://google.nl/maps/place/{location}/&amp;'
                    webbrowser.open(url)
                    self.speak(f'Here is the location {location}')
            
            # News
            elif 'news' in query:
                self.speak('Of course sir..')
                speak_news()
                self.speak('Do you want to read the full news...')
                test = self.listen()
                if test and 'yes' in test:
                    self.speak('Ok Sir, Opening browser...')
                    webbrowser.open(getNewsUrl())
                    self.speak('You can now read the full news from this website.')
                else:
                    self.speak('No Problem Sir')
            
            # Voice change
            elif 'voice' in query:
                voices = self.engine.getProperty('voices')
                if 'female' in query:
                    self.engine.setProperty('voice', voices[1].id)
                else:
                    self.engine.setProperty('voice', voices[0].id)
                self.speak("Hello Sir, I have switched my voice. How is it?")
            
            # System control
            elif 'shutdown' in query:
                self.speak("Shutting down system in 30 seconds, Sir")
                os.system("shutdown /s /t 30")
            
            elif 'restart' in query:
                self.speak("Restarting system in 30 seconds, Sir")
                os.system("shutdown /r /t 30")
            
            elif 'sleep' in query:
                self.speak("Putting system to sleep, Sir")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            
            elif 'lock' in query:
                self.speak("Locking system, Sir")
                os.system("rundll32.exe user32.dll,LockWorkStation")
            
            # Volume control
            elif 'volume up' in query:
                pyautogui.press('volumeup')
                self.speak("Volume increased, Sir")
            
            elif 'volume down' in query:
                pyautogui.press('volumedown')
                self.speak("Volume decreased, Sir")
            
            elif 'mute' in query:
                pyautogui.press('volumemute')
                self.speak("Audio muted, Sir")
            
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
                    with open('data.txt', 'w') as f:
                        f.write(remember_message)
            
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
                print(f"Error: {e}")
                self.speak("I encountered an error, Sir. Let's continue.")

def main():
    """Main function"""
    print("=" * 60)
    print("JARVIS Simple - Core Working Features")
    print("=" * 60)
    
    jarvis = SimpleJARVIS()
    jarvis.run()

if __name__ == "__main__":
    main()

