"""
JARVIS AI Brain Module
Advanced AI capabilities using OpenAI GPT
"""

import openai
import json
import requests
from datetime import datetime
from config import Config
import speech_recognition as sr
import pyttsx3

class AIBrain:
    def __init__(self):
        self.config = Config()
        self.client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.conversation_history = []
        self.user_preferences = self.load_preferences()
        
    def load_preferences(self):
        """Load user preferences from file"""
        try:
            with open('user_preferences.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "name": "Sir",
                "preferred_voice": "male",
                "interests": [],
                "schedule": {},
                "security_level": "high"
            }
    
    def save_preferences(self):
        """Save user preferences to file"""
        with open('user_preferences.json', 'w') as f:
            json.dump(self.user_preferences, f, indent=2)
    
    def process_command(self, user_input):
        """Process user command with AI understanding"""
        try:
            # Add context to the prompt
            context = f"""
            You are JARVIS, Tony Stark's AI assistant. You are highly intelligent, 
            witty, and capable of handling any task. The user is {self.user_preferences.get('name', 'Sir')}.
            
            Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Previous conversation: {self.conversation_history[-3:] if self.conversation_history else 'None'}
            
            User said: {user_input}
            
            Respond as JARVIS would - be helpful, intelligent, and slightly witty. 
            If the user asks for something you can do, acknowledge it and explain how you'll help.
            If it's something complex, break it down into steps.
            """
            
            response = self.client.chat.completions.create(
                model=self.config.AI_MODEL,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            ai_response = response.choices[0].message.content
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "jarvis": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, Sir. I'm experiencing some technical difficulties: {str(e)}"
    
    def analyze_intent(self, user_input):
        """Analyze user intent and categorize the request"""
        intents = {
            "system_control": ["shutdown", "restart", "sleep", "lock", "volume", "brightness"],
            "web_search": ["search", "google", "find", "look up", "what is"],
            "entertainment": ["play", "music", "video", "movie", "youtube", "netflix"],
            "productivity": ["schedule", "reminder", "calendar", "email", "document"],
            "information": ["weather", "news", "time", "date", "stock", "price"],
            "communication": ["call", "message", "email", "text", "contact"],
            "file_management": ["file", "folder", "document", "save", "delete", "organize"],
            "security": ["security", "lock", "encrypt", "backup", "scan"],
            "emergency": ["help", "emergency", "urgent", "911", "police", "fire"]
        }
        
        user_input_lower = user_input.lower()
        detected_intents = []
        
        for intent, keywords in intents.items():
            if any(keyword in user_input_lower for keyword in keywords):
                detected_intents.append(intent)
        
        return detected_intents
    
    def generate_response(self, user_input, intent_type=None):
        """Generate contextual response based on intent"""
        if intent_type == "emergency":
            return "Emergency protocols activated, Sir. What assistance do you require?"
        elif intent_type == "system_control":
            return "System control command recognized. Executing your request."
        elif intent_type == "web_search":
            return "Initiating web search protocols. What would you like me to find?"
        else:
            return self.process_command(user_input)
    
    def learn_from_interaction(self, user_input, response, user_feedback=None):
        """Learn from user interactions to improve responses"""
        if user_feedback:
            self.user_preferences["feedback"] = self.user_preferences.get("feedback", [])
            self.user_preferences["feedback"].append({
                "input": user_input,
                "response": response,
                "feedback": user_feedback,
                "timestamp": datetime.now().isoformat()
            })
            self.save_preferences()
    
    def get_smart_suggestions(self, context=""):
        """Provide smart suggestions based on context and time"""
        current_hour = datetime.now().hour
        
        suggestions = []
        
        if 6 <= current_hour < 12:
            suggestions.extend([
                "Would you like me to check today's schedule?",
                "Shall I provide the morning news briefing?",
                "Would you like me to check the weather for today?"
            ])
        elif 12 <= current_hour < 18:
            suggestions.extend([
                "Would you like me to check your afternoon meetings?",
                "Shall I organize your files?",
                "Would you like me to search for something?"
            ])
        else:
            suggestions.extend([
                "Would you like me to prepare tomorrow's schedule?",
                "Shall I run a system security check?",
                "Would you like me to backup your important files?"
            ])
        
        return suggestions[:3]  # Return top 3 suggestions
