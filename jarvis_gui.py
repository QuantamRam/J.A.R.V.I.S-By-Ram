"""
JARVIS GUI Interface
Modern holographic-style interface for JARVIS
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
import json
from config import Config
from enhanced_voice import EnhancedVoiceSystem
from ai_brain import AIBrain
from smart_automation import SmartAutomation

class JARVISGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.config = Config()
        self.voice_system = EnhancedVoiceSystem()
        self.ai_brain = AIBrain()
        self.automation = SmartAutomation()
        
        self.setup_gui()
        self.is_listening = False
        self.conversation_history = []
        
    def setup_gui(self):
        """Setup the main GUI interface"""
        self.root.title("J.A.R.V.I.S - Just A Rather Very Intelligent System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('JARVIS.TLabel', background='#0a0a0a', foreground='#00ff00', font=('Consolas', 12))
        style.configure('JARVIS.TButton', background='#1a1a1a', foreground='#00ff00', font=('Consolas', 10))
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#0a0a0a')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="J.A.R.V.I.S", 
                              font=('Consolas', 24, 'bold'), 
                              fg='#00ff00', bg='#0a0a0a')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Just A Rather Very Intelligent System", 
                                 font=('Consolas', 12), 
                                 fg='#00ff88', bg='#0a0a0a')
        subtitle_label.pack()
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#0a0a0a')
        status_frame.pack(fill='x', pady=(0, 20))
        
        self.status_label = tk.Label(status_frame, text="Status: Standby", 
                                    font=('Consolas', 12), 
                                    fg='#ffff00', bg='#0a0a0a')
        self.status_label.pack(side='left')
        
        self.time_label = tk.Label(status_frame, text="", 
                                  font=('Consolas', 12), 
                                  fg='#00ff00', bg='#0a0a0a')
        self.time_label.pack(side='right')
        
        # Conversation area
        conv_frame = tk.Frame(main_frame, bg='#0a0a0a')
        conv_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        conv_label = tk.Label(conv_frame, text="Conversation Log", 
                             font=('Consolas', 14, 'bold'), 
                             fg='#00ff00', bg='#0a0a0a')
        conv_label.pack(anchor='w', pady=(0, 10))
        
        self.conversation_text = scrolledtext.ScrolledText(
            conv_frame, 
            height=15, 
            bg='#1a1a1a', 
            fg='#00ff00', 
            font=('Consolas', 11),
            insertbackground='#00ff00',
            selectbackground='#003300'
        )
        self.conversation_text.pack(fill='both', expand=True)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#0a0a0a')
        control_frame.pack(fill='x', pady=(0, 20))
        
        # Voice control buttons
        voice_frame = tk.Frame(control_frame, bg='#0a0a0a')
        voice_frame.pack(side='left', padx=(0, 20))
        
        self.listen_button = tk.Button(voice_frame, text="🎤 Start Listening", 
                                      command=self.toggle_listening,
                                      bg='#1a1a1a', fg='#00ff00', 
                                      font=('Consolas', 10),
                                      relief='raised', bd=2)
        self.listen_button.pack(side='left', padx=(0, 10))
        
        self.voice_auth_button = tk.Button(voice_frame, text="🔐 Voice Auth", 
                                          command=self.voice_authentication,
                                          bg='#1a1a1a', fg='#00ff00', 
                                          font=('Consolas', 10),
                                          relief='raised', bd=2)
        self.voice_auth_button.pack(side='left')
        
        # System control buttons
        system_frame = tk.Frame(control_frame, bg='#0a0a0a')
        system_frame.pack(side='left', padx=(0, 20))
        
        self.system_button = tk.Button(system_frame, text="⚙️ System Control", 
                                       command=self.open_system_control,
                                       bg='#1a1a1a', fg='#00ff00', 
                                       font=('Consolas', 10),
                                       relief='raised', bd=2)
        self.system_button.pack(side='left', padx=(0, 10))
        
        self.automation_button = tk.Button(system_frame, text="🤖 Automation", 
                                          command=self.open_automation_panel,
                                          bg='#1a1a1a', fg='#00ff00', 
                                          font=('Consolas', 10),
                                          relief='raised', bd=2)
        self.automation_button.pack(side='left')
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#0a0a0a')
        input_frame.pack(fill='x')
        
        input_label = tk.Label(input_frame, text="Command Input:", 
                              font=('Consolas', 12), 
                              fg='#00ff00', bg='#0a0a0a')
        input_label.pack(anchor='w', pady=(0, 5))
        
        self.command_entry = tk.Entry(input_frame, 
                                     bg='#1a1a1a', fg='#00ff00', 
                                     font=('Consolas', 11),
                                     insertbackground='#00ff00')
        self.command_entry.pack(fill='x', pady=(0, 10))
        self.command_entry.bind('<Return>', self.process_command)
        
        self.send_button = tk.Button(input_frame, text="Send Command", 
                                    command=self.process_command,
                                    bg='#1a1a1a', fg='#00ff00', 
                                    font=('Consolas', 10),
                                    relief='raised', bd=2)
        self.send_button.pack(anchor='e')
        
        # Start time update
        self.update_time()
        
        # Add welcome message
        self.add_to_conversation("JARVIS", "System initialized. Ready for your commands, Sir.")
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Time: {current_time}")
        self.root.after(1000, self.update_time)
    
    def add_to_conversation(self, speaker, message):
        """Add message to conversation log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {speaker}: {message}\n"
        
        self.conversation_text.insert(tk.END, formatted_message)
        self.conversation_text.see(tk.END)
        
        # Store in history
        self.conversation_history.append({
            "timestamp": timestamp,
            "speaker": speaker,
            "message": message
        })
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(text="🔇 Stop Listening", bg='#2a1a1a')
            self.status_label.config(text="Status: Listening...", fg='#ff0000')
            
            # Start listening in separate thread
            threading.Thread(target=self.voice_listening_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.listen_button.config(text="🎤 Start Listening", bg='#1a1a1a')
            self.status_label.config(text="Status: Standby", fg='#ffff00')
            self.voice_system.stop_listening()
    
    def voice_listening_loop(self):
        """Voice listening loop"""
        while self.is_listening:
            try:
                command = self.voice_system.listen_for_wake_word()
                if command:
                    self.add_to_conversation("You", command)
                    response = self.process_voice_command(command)
                    self.add_to_conversation("JARVIS", response)
                    self.voice_system.speak(response)
            except Exception as e:
                self.add_to_conversation("System", f"Voice error: {str(e)}")
                time.sleep(1)
    
    def voice_authentication(self):
        """Voice authentication"""
        self.add_to_conversation("JARVIS", "Initiating voice authentication...")
        
        def auth_thread():
            success = self.voice_system.voice_authentication()
            if success:
                self.add_to_conversation("JARVIS", "Authentication successful, Sir")
                self.status_label.config(text="Status: Authenticated", fg='#00ff00')
            else:
                self.add_to_conversation("JARVIS", "Authentication failed")
                self.status_label.config(text="Status: Authentication Failed", fg='#ff0000')
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    def process_command(self, event=None):
        """Process text command"""
        command = self.command_entry.get().strip()
        if command:
            self.add_to_conversation("You", command)
            response = self.process_voice_command(command)
            self.add_to_conversation("JARVIS", response)
            self.command_entry.delete(0, tk.END)
    
    def process_voice_command(self, command):
        """Process voice or text command"""
        try:
            # Analyze intent
            intents = self.ai_brain.analyze_intent(command)
            
            # Process based on intent
            if "system_control" in intents:
                if "shutdown" in command:
                    response = self.automation.system_control("shutdown")
                elif "restart" in command:
                    response = self.automation.system_control("restart")
                elif "sleep" in command:
                    response = self.automation.system_control("sleep")
                elif "lock" in command:
                    response = self.automation.system_control("lock")
                else:
                    response = self.ai_brain.process_command(command)
            elif "file_management" in intents:
                if "organize" in command:
                    response = self.automation.smart_file_management("organize_desktop")
                elif "cleanup" in command:
                    response = self.automation.smart_file_management("cleanup_temp")
                elif "backup" in command:
                    response = self.automation.smart_file_management("backup_important")
                else:
                    response = self.ai_brain.process_command(command)
            else:
                response = self.ai_brain.process_command(command)
            
            return response
            
        except Exception as e:
            return f"I apologize, Sir. An error occurred: {str(e)}"
    
    def open_system_control(self):
        """Open system control panel"""
        control_window = tk.Toplevel(self.root)
        control_window.title("System Control Panel")
        control_window.geometry("400x300")
        control_window.configure(bg='#0a0a0a')
        
        # System control buttons
        tk.Button(control_window, text="Shutdown", 
                 command=lambda: self.automation.system_control("shutdown"),
                 bg='#1a1a1a', fg='#ff0000', font=('Consolas', 10)).pack(pady=5)
        
        tk.Button(control_window, text="Restart", 
                 command=lambda: self.automation.system_control("restart"),
                 bg='#1a1a1a', fg='#ff8800', font=('Consolas', 10)).pack(pady=5)
        
        tk.Button(control_window, text="Sleep", 
                 command=lambda: self.automation.system_control("sleep"),
                 bg='#1a1a1a', fg='#0088ff', font=('Consolas', 10)).pack(pady=5)
        
        tk.Button(control_window, text="Lock", 
                 command=lambda: self.automation.system_control("lock"),
                 bg='#1a1a1a', fg='#8800ff', font=('Consolas', 10)).pack(pady=5)
    
    def open_automation_panel(self):
        """Open automation panel"""
        automation_window = tk.Toplevel(self.root)
        automation_window.title("Automation Panel")
        automation_window.geometry("500x400")
        automation_window.configure(bg='#0a0a0a')
        
        # Automation controls
        tk.Label(automation_window, text="Automation Controls", 
                font=('Consolas', 16, 'bold'), 
                fg='#00ff00', bg='#0a0a0a').pack(pady=10)
        
        tk.Button(automation_window, text="Organize Desktop", 
                 command=lambda: self.automation.smart_file_management("organize_desktop"),
                 bg='#1a1a1a', fg='#00ff00', font=('Consolas', 10)).pack(pady=5)
        
        tk.Button(automation_window, text="Cleanup Temp Files", 
                 command=lambda: self.automation.smart_file_management("cleanup_temp"),
                 bg='#1a1a1a', fg='#00ff00', font=('Consolas', 10)).pack(pady=5)
        
        tk.Button(automation_window, text="Backup Important Files", 
                 command=lambda: self.automation.smart_file_management("backup_important"),
                 bg='#1a1a1a', fg='#00ff00', font=('Consolas', 10)).pack(pady=5)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = JARVISGUI()
    app.run()

