"""
Enhanced JARVIS - Iron Man Style AI Assistant
Advanced AI capabilities with modern interface and automation
"""

import os
import sys
import threading
import time
from datetime import datetime
import cv2
import json
from config import Config
from enhanced_voice import EnhancedVoiceSystem
from ai_brain import AIBrain
from smart_automation import SmartAutomation
from jarvis_gui import JARVISGUI
from advanced_features import AdvancedFeatures
from learning_system import LearningSystem
from emergency_security import EmergencySecuritySystem

# Import original modules
from helpers import *
from news import speak_news, getNewsUrl
from OCR import OCR
from diction import translate
from youtube import youtube

class EnhancedJARVIS:
    def __init__(self):
        self.config = Config()
        self.voice_system = EnhancedVoiceSystem()
        self.ai_brain = AIBrain()
        self.automation = SmartAutomation()
        self.advanced_features = AdvancedFeatures()
        self.learning_system = LearningSystem()
        self.emergency_security = EmergencySecuritySystem()
        
        # Initialize face recognition
        self.setup_face_recognition()
        
        # System status
        self.is_authenticated = False
        self.is_active = False
        self.security_level = self.config.SECURITY_LEVEL
        
        # Start automation scheduler
        self.automation.start_scheduler()
        
        print("JARVIS Enhanced System Initialized")
    
    def setup_face_recognition(self):
        """Setup face recognition system"""
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read('./Face-Recognition/trainer/trainer.yml')
            self.cascadePath = "./Face-Recognition/haarcascade_frontalface_default.xml"
            self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
            self.font = cv2.FONT_HERSHEY_SIMPLEX
            self.names = ['', 'Sir']  # Update with actual user names
            print("Face recognition system loaded")
        except Exception as e:
            print(f"Face recognition setup error: {e}")
            self.recognizer = None
    
    def authenticate_user(self):
        """Enhanced authentication system"""
        print("Initiating authentication protocols...")
        
        if self.security_level == "high":
            # Multi-factor authentication
            if self.face_recognition_auth():
                if self.voice_authentication():
                    self.is_authenticated = True
                    self.voice_system.speak("Authentication successful. Welcome, Sir.")
                    return True
                else:
                    self.voice_system.speak("Voice authentication failed.")
                    return False
            else:
                self.voice_system.speak("Face recognition failed.")
                return False
        else:
            # Simple authentication
            if self.voice_authentication():
                self.is_authenticated = True
                self.voice_system.speak("Welcome, Sir.")
                return True
            return False
    
    def face_recognition_auth(self):
        """Face recognition authentication"""
        if not self.recognizer:
            return True  # Skip if face recognition not available
        
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)
        
        self.voice_system.speak("Please look at the camera for face recognition.")
        
        attempts = 0
        max_attempts = 5
        
        while attempts < max_attempts:
            ret, img = cam.read()
            converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            faces = self.faceCascade.detectMultiScale(
                converted_image,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                id, accuracy = self.recognizer.predict(converted_image[y:y + h, x:x + w])
                
                if accuracy < 100:
                    cam.release()
                    cv2.destroyAllWindows()
                    return True
                else:
                    attempts += 1
                    time.sleep(1)
            
            cv2.imshow('Face Recognition', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cam.release()
        cv2.destroyAllWindows()
        return False
    
    def voice_authentication(self):
        """Voice authentication"""
        return self.voice_system.voice_authentication()
    
    def wish_me(self):
        """Enhanced greeting system"""
        hour = int(datetime.now().hour)
        
        if 0 <= hour < 12:
            greeting = "Good Morning, Sir"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon, Sir"
        else:
            greeting = "Good Evening, Sir"
        
        self.voice_system.speak(greeting)
        
        # Get weather and system status
        try:
            weather()
            self.get_system_status()
        except:
            pass
        
        self.voice_system.speak("I am JARVIS Enhanced. How may I assist you today, Sir?")
    
    def get_system_status(self):
        """Get comprehensive system status"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = f"System Status: CPU at {cpu_percent}%, Memory at {memory.percent}%, Disk at {disk.percent}%"
            self.voice_system.speak(status)
        except Exception as e:
            print(f"System status error: {e}")
    
    def execute_enhanced_query(self, query):
        """Enhanced query execution with AI integration"""
        try:
            # Analyze intent
            intents = self.ai_brain.analyze_intent(query)
            
            # Process based on intent
            if "emergency" in intents:
                return self.handle_emergency(query)
            elif "system_control" in intents:
                return self.handle_system_control(query)
            elif "file_management" in intents:
                return self.handle_file_management(query)
            elif "web_search" in intents:
                return self.handle_web_search(query)
            elif "entertainment" in intents:
                return self.handle_entertainment(query)
            elif "productivity" in intents:
                return self.handle_productivity(query)
            elif "information" in intents:
                return self.handle_information(query)
            elif "communication" in intents:
                return self.handle_communication(query)
            elif "calendar" in query.lower():
                return self.handle_calendar(query)
            elif "email" in query.lower():
                return self.handle_email_advanced(query)
            elif "web" in query.lower() and "scrape" in query.lower():
                return self.handle_web_scraping(query)
            elif "learning" in query.lower() or "insights" in query.lower():
                return self.handle_learning(query)
            elif "emergency" in query.lower():
                return self.handle_emergency_advanced(query)
            else:
                # Use AI brain for general conversation
                response = self.ai_brain.process_command(query)
                
                # Record interaction for learning
                self.learning_system.record_interaction(query, response)
                
                return response
                
        except Exception as e:
            return f"I apologize, Sir. An error occurred: {str(e)}"
    
    def handle_emergency(self, query):
        """Handle emergency situations"""
        self.voice_system.speak("Emergency protocols activated, Sir. What assistance do you require?")
        
        # Implement emergency procedures
        if "police" in query or "911" in query:
            self.voice_system.speak("Contacting emergency services...")
            # Add actual emergency contact functionality
        elif "fire" in query:
            self.voice_system.speak("Fire emergency detected. Initiating safety protocols...")
        elif "medical" in query:
            self.voice_system.speak("Medical emergency detected. Contacting medical services...")
        
        return "Emergency protocols activated"
    
    def handle_system_control(self, query):
        """Handle system control commands"""
        if "shutdown" in query:
            return self.automation.system_control("shutdown")
        elif "restart" in query:
            return self.automation.system_control("restart")
        elif "sleep" in query:
            return self.automation.system_control("sleep")
        elif "lock" in query:
            return self.automation.system_control("lock")
        elif "volume" in query:
            if "up" in query:
                return self.automation.system_control("volume_up")
            elif "down" in query:
                return self.automation.system_control("volume_down")
            elif "mute" in query:
                return self.automation.system_control("mute")
        else:
            return self.ai_brain.process_command(query)
    
    def handle_file_management(self, query):
        """Handle file management commands"""
        if "organize" in query:
            return self.automation.smart_file_management("organize_desktop")
        elif "cleanup" in query or "clean" in query:
            return self.automation.smart_file_management("cleanup_temp")
        elif "backup" in query:
            return self.automation.smart_file_management("backup_important")
        elif "find" in query:
            # Extract filename from query
            words = query.split()
            if "file" in words:
                file_index = words.index("file")
                if file_index + 1 < len(words):
                    filename = words[file_index + 1]
                    return self.automation.smart_file_management("find_file", filename)
        else:
            return self.ai_brain.process_command(query)
    
    def handle_web_search(self, query):
        """Handle web search commands"""
        if "search" in query:
            self.voice_system.speak("What would you like me to search for?")
            search_term = self.voice_system.listen_for_command()
            if search_term:
                url = f'https://google.com/search?q={search_term}'
                webbrowser.open(url)
                return f"Searching for {search_term}"
        elif "youtube" in query:
            self.voice_system.speak("What would you like to search on YouTube?")
            search_term = self.voice_system.listen_for_command()
            if search_term:
                youtube(search_term)
                return f"Searching YouTube for {search_term}"
        else:
            return self.ai_brain.process_command(query)
    
    def handle_entertainment(self, query):
        """Handle entertainment commands"""
        if "play music" in query:
            # Enhanced music playing
            music_path = self.config.MUSIC_PATH
            if os.path.exists(music_path):
                os.startfile(music_path)
                return "Playing music, Sir"
            else:
                return "Music directory not found, Sir"
        elif "joke" in query:
            joke()
            return "Telling jokes, Sir"
        else:
            return self.ai_brain.process_command(query)
    
    def handle_productivity(self, query):
        """Handle productivity commands"""
        if "schedule" in query:
            return self.automation.smart_scheduling("daily_task", "daily", "morning_routine")
        elif "reminder" in query:
            self.voice_system.speak("What would you like me to remind you about?")
            reminder = self.voice_system.listen_for_command()
            if reminder:
                # Implement reminder system
                return f"Reminder set: {reminder}"
        elif "email" in query:
            return self.handle_email(query)
        else:
            return self.ai_brain.process_command(query)
    
    def handle_information(self, query):
        """Handle information requests"""
        if "news" in query:
            speak_news()
            return "News briefing complete, Sir"
        elif "weather" in query:
            weather()
            return "Weather information provided, Sir"
        elif "time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            self.voice_system.speak(f"The time is {strTime}")
            return f"Current time: {strTime}"
        elif "wikipedia" in query:
            self.voice_system.speak("What would you like to know about?")
            topic = self.voice_system.listen_for_command()
            if topic:
                try:
                    results = wikipedia.summary(topic, sentences=2)
                    self.voice_system.speak(f"According to Wikipedia: {results}")
                    return f"Wikipedia information: {results}"
                except:
                    return "Unable to find information on that topic"
        else:
            return self.ai_brain.process_command(query)
    
    def handle_email(self, query):
        """Handle email commands"""
        try:
            self.voice_system.speak("What should I say in the email?")
            content = self.voice_system.listen_for_command()
            if content:
                # Implement email sending
                to = self.config.EMAIL_USERNAME
                # Add actual email sending functionality
                return f"Email sent: {content}"
        except Exception as e:
            return f"Email error: {str(e)}"
    
    def handle_communication(self, query):
        """Handle communication commands"""
        try:
            if "call" in query:
                self.voice_system.speak("Calling functionality not yet implemented, Sir")
                return "Call feature coming soon"
            elif "message" in query:
                self.voice_system.speak("Messaging functionality not yet implemented, Sir")
                return "Messaging feature coming soon"
            else:
                return self.ai_brain.process_command(query)
        except Exception as e:
            return f"Communication error: {str(e)}"
    
    def handle_calendar(self, query):
        """Handle calendar commands"""
        try:
            if "add event" in query or "schedule" in query:
                self.voice_system.speak("What event would you like to add?")
                event_title = self.voice_system.listen_for_command()
                if event_title:
                    return self.advanced_features.calendar_integration("add_event", title=event_title)
            elif "today" in query:
                return self.advanced_features.calendar_integration("get_today_events")
            elif "upcoming" in query:
                return self.advanced_features.calendar_integration("get_upcoming_events")
            else:
                return self.ai_brain.process_command(query)
        except Exception as e:
            return f"Calendar error: {str(e)}"
    
    def handle_email_advanced(self, query):
        """Handle advanced email commands"""
        try:
            if "send" in query:
                self.voice_system.speak("Who should I send the email to?")
                recipient = self.voice_system.listen_for_command()
                if recipient:
                    self.voice_system.speak("What should the subject be?")
                    subject = self.voice_system.listen_for_command()
                    if subject:
                        self.voice_system.speak("What should I say in the email?")
                        body = self.voice_system.listen_for_command()
                        if body:
                            return self.advanced_features.email_automation("send_email", 
                                                                          to=recipient, 
                                                                          subject=subject, 
                                                                          body=body)
            elif "schedule" in query:
                self.voice_system.speak("Email scheduling feature coming soon, Sir")
                return "Email scheduling feature coming soon"
            else:
                return self.ai_brain.process_command(query)
        except Exception as e:
            return f"Advanced email error: {str(e)}"
    
    def handle_web_scraping(self, query):
        """Handle web scraping commands"""
        try:
            if "news" in query:
                return self.advanced_features.web_scraping("scrape_news")
            elif "weather" in query:
                self.voice_system.speak("What location?")
                location = self.voice_system.listen_for_command()
                if location:
                    return self.advanced_features.web_scraping("scrape_weather", location=location)
            elif "stock" in query:
                self.voice_system.speak("What stock symbol?")
                symbol = self.voice_system.listen_for_command()
                if symbol:
                    return self.advanced_features.web_scraping("scrape_stock", symbol=symbol.upper())
            else:
                return self.ai_brain.process_command(query)
        except Exception as e:
            return f"Web scraping error: {str(e)}"
    
    def handle_learning(self, query):
        """Handle learning and insights commands"""
        try:
            if "insights" in query or "analyze" in query:
                return self.learning_system.get_user_insights()
            elif "suggestions" in query or "improve" in query:
                suggestions = self.learning_system.suggest_improvements()
                return f"Improvement suggestions: {'; '.join(suggestions)}"
            elif "reset" in query and "learning" in query:
                return self.learning_system.reset_learning_data()
            elif "export" in query:
                return self.learning_system.export_learning_data()
            else:
                return self.ai_brain.process_command(query)
        except Exception as e:
            return f"Learning system error: {str(e)}"
    
    def handle_emergency_advanced(self, query):
        """Handle advanced emergency commands"""
        try:
            if "medical" in query:
                self.emergency_security.emergency_protocol("medical")
                return "Medical emergency protocols activated"
            elif "fire" in query:
                self.emergency_security.emergency_protocol("fire")
                return "Fire emergency protocols activated"
            elif "security" in query:
                self.emergency_security.emergency_protocol("security")
                return "Security emergency protocols activated"
            elif "system" in query:
                self.emergency_security.emergency_protocol("system")
                return "System emergency protocols activated"
            elif "add contact" in query:
                self.voice_system.speak("What type of emergency contact?")
                contact_type = self.voice_system.listen_for_command()
                if contact_type:
                    self.voice_system.speak("What is the contact information?")
                    contact_info = self.voice_system.listen_for_command()
                    if contact_info:
                        return self.emergency_security.add_emergency_contact(contact_type, contact_info)
            elif "security report" in query:
                return self.emergency_security.get_security_report()
            elif "deactivate" in query:
                return self.emergency_security.deactivate_emergency_mode()
            else:
                return self.ai_brain.process_command(query)
        except Exception as e:
            return f"Emergency system error: {str(e)}"
    
    def run_gui_mode(self):
        """Run JARVIS in GUI mode"""
        gui = JARVISGUI()
        gui.run()
    
    def run_voice_mode(self):
        """Run JARVIS in voice-only mode"""
        if not self.is_authenticated:
            if not self.authenticate_user():
                print("Authentication failed. Exiting.")
                return
        
        self.wish_me()
        
        while True:
            try:
                query = self.voice_system.listen_for_wake_word()
                if query:
                    response = self.execute_enhanced_query(query)
                    self.voice_system.speak(response)
            except KeyboardInterrupt:
                self.voice_system.speak("Goodbye, Sir.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
    
    def run_continuous_mode(self):
        """Run JARVIS in continuous listening mode"""
        if not self.is_authenticated:
            if not self.authenticate_user():
                print("Authentication failed. Exiting.")
                return
        
        self.wish_me()
        self.voice_system.speak("Continuous listening mode activated, Sir.")
        
        for command in self.voice_system.continuous_listening():
            response = self.execute_enhanced_query(command)
            self.voice_system.speak(response)

def main():
    """Main function to run JARVIS"""
    print("Initializing JARVIS Enhanced System...")
    
    jarvis = EnhancedJARVIS()
    
    # Check command line arguments for mode
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "gui":
            jarvis.run_gui_mode()
        elif mode == "voice":
            jarvis.run_voice_mode()
        elif mode == "continuous":
            jarvis.run_continuous_mode()
        else:
            print("Invalid mode. Use: gui, voice, or continuous")
    else:
        # Default to GUI mode
        jarvis.run_gui_mode()

if __name__ == "__main__":
    main()
