"""
JARVIS Learning System
Machine learning for user preferences and adaptive responses
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import pickle
import os
from collections import defaultdict, Counter
import re

class LearningSystem:
    def __init__(self):
        self.user_data_file = 'user_learning_data.json'
        self.model_file = 'jarvis_model.pkl'
        self.user_data = self.load_user_data()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.preference_model = None
        self.load_model()
        
    def load_user_data(self):
        """Load user interaction data"""
        try:
            with open(self.user_data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "interactions": [],
                "preferences": {
                    "voice_speed": 200,
                    "voice_volume": 0.8,
                    "preferred_voice": "male",
                    "common_commands": [],
                    "time_patterns": {},
                    "interests": [],
                    "dislikes": []
                },
                "learning_stats": {
                    "total_interactions": 0,
                    "accuracy_score": 0.0,
                    "last_updated": None
                }
            }
    
    def save_user_data(self):
        """Save user data to file"""
        with open(self.user_data_file, 'w') as f:
            json.dump(self.user_data, f, indent=2)
    
    def load_model(self):
        """Load trained model"""
        try:
            with open(self.model_file, 'rb') as f:
                self.preference_model = pickle.load(f)
        except FileNotFoundError:
            self.preference_model = None
    
    def save_model(self):
        """Save trained model"""
        with open(self.model_file, 'wb') as f:
            pickle.dump(self.preference_model, f)
    
    def record_interaction(self, user_input, jarvis_response, user_feedback=None, execution_time=None):
        """Record user interaction for learning"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "jarvis_response": jarvis_response,
            "user_feedback": user_feedback,
            "execution_time": execution_time,
            "hour": datetime.now().hour,
            "day_of_week": datetime.now().weekday(),
            "success": user_feedback is None or user_feedback.lower() in ['good', 'yes', 'correct', 'thanks']
        }
        
        self.user_data["interactions"].append(interaction)
        self.user_data["learning_stats"]["total_interactions"] += 1
        self.user_data["learning_stats"]["last_updated"] = datetime.now().isoformat()
        
        # Update preferences based on interaction
        self.update_preferences(interaction)
        
        # Save data
        self.save_user_data()
        
        # Retrain model periodically
        if len(self.user_data["interactions"]) % 10 == 0:
            self.train_model()
    
    def update_preferences(self, interaction):
        """Update user preferences based on interaction"""
        user_input = interaction["user_input"].lower()
        
        # Extract common commands
        if interaction["success"]:
            self.extract_common_commands(user_input)
        
        # Update time patterns
        hour = interaction["hour"]
        day = interaction["day_of_week"]
        
        if hour not in self.user_data["preferences"]["time_patterns"]:
            self.user_data["preferences"]["time_patterns"][hour] = 0
        self.user_data["preferences"]["time_patterns"][hour] += 1
        
        # Extract interests
        self.extract_interests(user_input)
        
        # Update voice preferences based on feedback
        if interaction["user_feedback"]:
            feedback = interaction["user_feedback"].lower()
            if "slow" in feedback or "faster" in feedback:
                self.user_data["preferences"]["voice_speed"] += 10
            elif "fast" in feedback or "slower" in feedback:
                self.user_data["preferences"]["voice_speed"] -= 10
            
            if "loud" in feedback or "louder" in feedback:
                self.user_data["preferences"]["voice_volume"] += 0.1
            elif "quiet" in feedback or "quieter" in feedback:
                self.user_data["preferences"]["voice_volume"] -= 0.1
    
    def extract_common_commands(self, user_input):
        """Extract common command patterns"""
        # Simple command extraction
        commands = re.findall(r'\b(open|search|play|send|create|find|show|tell)\b', user_input)
        
        for command in commands:
            if command not in self.user_data["preferences"]["common_commands"]:
                self.user_data["preferences"]["common_commands"].append(command)
    
    def extract_interests(self, user_input):
        """Extract user interests from interactions"""
        interest_keywords = {
            "technology": ["tech", "computer", "programming", "software", "ai", "robot"],
            "music": ["music", "song", "play", "artist", "album", "concert"],
            "news": ["news", "headlines", "current", "events", "politics"],
            "weather": ["weather", "temperature", "rain", "sunny", "forecast"],
            "sports": ["sports", "game", "team", "player", "match", "score"],
            "movies": ["movie", "film", "cinema", "actor", "director", "watch"],
            "travel": ["travel", "trip", "vacation", "hotel", "flight", "destination"],
            "food": ["food", "restaurant", "recipe", "cook", "eat", "meal"]
        }
        
        for category, keywords in interest_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                if category not in self.user_data["preferences"]["interests"]:
                    self.user_data["preferences"]["interests"].append(category)
    
    def train_model(self):
        """Train machine learning model for user preferences"""
        try:
            if len(self.user_data["interactions"]) < 5:
                return  # Need more data
            
            # Prepare training data
            interactions = self.user_data["interactions"]
            texts = [interaction["user_input"] for interaction in interactions]
            labels = [1 if interaction["success"] else 0 for interaction in interactions]
            
            # Vectorize texts
            X = self.vectorizer.fit_transform(texts)
            
            # Train simple clustering model
            if len(set(labels)) > 1:  # Need at least 2 different labels
                self.preference_model = KMeans(n_clusters=2, random_state=42)
                self.preference_model.fit(X)
                
                # Calculate accuracy
                predictions = self.preference_model.predict(X)
                accuracy = np.mean(predictions == labels)
                self.user_data["learning_stats"]["accuracy_score"] = accuracy
                
                # Save model
                self.save_model()
                
        except Exception as e:
            print(f"Model training error: {e}")
    
    def predict_user_intent(self, user_input):
        """Predict user intent based on learned patterns"""
        try:
            if not self.preference_model:
                return None
            
            # Vectorize input
            X = self.vectorizer.transform([user_input])
            
            # Predict cluster
            cluster = self.preference_model.predict(X)[0]
            
            # Find similar successful interactions
            similar_interactions = []
            for interaction in self.user_data["interactions"]:
                if interaction["success"]:
                    interaction_vector = self.vectorizer.transform([interaction["user_input"]])
                    similarity = cosine_similarity(X, interaction_vector)[0][0]
                    if similarity > 0.3:  # Threshold for similarity
                        similar_interactions.append((interaction, similarity))
            
            # Sort by similarity
            similar_interactions.sort(key=lambda x: x[1], reverse=True)
            
            return similar_interactions[:3]  # Return top 3 similar interactions
            
        except Exception as e:
            print(f"Intent prediction error: {e}")
            return None
    
    def get_personalized_response(self, user_input):
        """Generate personalized response based on learned preferences"""
        try:
            # Get similar successful interactions
            similar_interactions = self.predict_user_intent(user_input)
            
            if similar_interactions:
                # Use the most similar successful interaction as template
                best_match = similar_interactions[0][0]
                return best_match["jarvis_response"]
            
            # Fallback to preference-based response
            return self.get_preference_based_response(user_input)
            
        except Exception as e:
            print(f"Personalized response error: {e}")
            return None
    
    def get_preference_based_response(self, user_input):
        """Generate response based on user preferences"""
        user_input_lower = user_input.lower()
        
        # Check for common commands
        common_commands = self.user_data["preferences"]["common_commands"]
        for command in common_commands:
            if command in user_input_lower:
                return f"I'll {command} that for you, Sir."
        
        # Check for interests
        interests = self.user_data["preferences"]["interests"]
        for interest in interests:
            if interest in user_input_lower:
                return f"I know you're interested in {interest}, Sir. Let me help you with that."
        
        return None
    
    def get_user_insights(self):
        """Generate insights about user behavior"""
        try:
            interactions = self.user_data["interactions"]
            if not interactions:
                return "No interaction data available yet."
            
            # Analyze time patterns
            hours = [interaction["hour"] for interaction in interactions]
            most_active_hour = Counter(hours).most_common(1)[0][0]
            
            # Analyze success rate
            successful_interactions = sum(1 for i in interactions if i["success"])
            success_rate = (successful_interactions / len(interactions)) * 100
            
            # Analyze common commands
            common_commands = self.user_data["preferences"]["common_commands"]
            
            # Analyze interests
            interests = self.user_data["preferences"]["interests"]
            
            insights = f"""
            User Insights:
            - Most active hour: {most_active_hour}:00
            - Success rate: {success_rate:.1f}%
            - Common commands: {', '.join(common_commands[:5])}
            - Interests: {', '.join(interests[:5])}
            - Total interactions: {len(interactions)}
            """
            
            return insights
            
        except Exception as e:
            return f"Insights generation error: {e}"
    
    def suggest_improvements(self):
        """Suggest improvements based on learning data"""
        try:
            suggestions = []
            
            # Check success rate
            interactions = self.user_data["interactions"]
            if interactions:
                success_rate = sum(1 for i in interactions if i["success"]) / len(interactions)
                
                if success_rate < 0.7:
                    suggestions.append("Consider improving voice recognition accuracy")
                
                if success_rate < 0.5:
                    suggestions.append("Review common failure patterns")
            
            # Check voice preferences
            voice_speed = self.user_data["preferences"]["voice_speed"]
            if voice_speed > 250:
                suggestions.append("Voice speed might be too fast")
            elif voice_speed < 150:
                suggestions.append("Voice speed might be too slow")
            
            # Check interaction patterns
            if len(interactions) < 10:
                suggestions.append("Need more interaction data for better learning")
            
            return suggestions if suggestions else ["System is performing well"]
            
        except Exception as e:
            return [f"Improvement analysis error: {e}"]
    
    def adaptive_learning(self, user_input, context=None):
        """Adaptive learning based on current context"""
        try:
            # Get current time context
            current_hour = datetime.now().hour
            current_day = datetime.now().weekday()
            
            # Adjust response based on time patterns
            time_patterns = self.user_data["preferences"]["time_patterns"]
            if current_hour in time_patterns:
                # User is active at this time, use learned preferences
                return self.get_personalized_response(user_input)
            else:
                # Unusual time, use general response
                return None
            
        except Exception as e:
            print(f"Adaptive learning error: {e}")
            return None
    
    def export_learning_data(self, filename=None):
        """Export learning data for analysis"""
        try:
            if not filename:
                filename = f"jarvis_learning_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.user_data, f, indent=2)
            
            return f"Learning data exported to {filename}"
            
        except Exception as e:
            return f"Export error: {e}"
    
    def reset_learning_data(self):
        """Reset all learning data"""
        try:
            self.user_data = {
                "interactions": [],
                "preferences": {
                    "voice_speed": 200,
                    "voice_volume": 0.8,
                    "preferred_voice": "male",
                    "common_commands": [],
                    "time_patterns": {},
                    "interests": [],
                    "dislikes": []
                },
                "learning_stats": {
                    "total_interactions": 0,
                    "accuracy_score": 0.0,
                    "last_updated": None
                }
            }
            
            self.save_user_data()
            
            # Remove model file
            if os.path.exists(self.model_file):
                os.remove(self.model_file)
            
            return "Learning data reset successfully"
            
        except Exception as e:
            return f"Reset error: {e}"
