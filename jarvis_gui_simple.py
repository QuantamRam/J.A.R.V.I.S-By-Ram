"""
JARVIS Simple GUI - Basic Interface
Simple GUI version of JARVIS with core features
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
from jarvis_simple import SimpleJARVIS

class JARVISSimpleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.jarvis = SimpleJARVIS()
        self.is_listening = False
        self.conversation_history = []
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root.title("JARVIS Simple - Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#1a1a1a')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="J.A.R.V.I.S", 
                              font=('Arial', 24, 'bold'), 
                              fg='#00ff00', bg='#1a1a1a')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Just A Rather Very Intelligent System", 
                                 font=('Arial', 12), 
                                 fg='#00ff88', bg='#1a1a1a')
        subtitle_label.pack()
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#1a1a1a')
        status_frame.pack(fill='x', pady=(0, 20))
        
        self.status_label = tk.Label(status_frame, text="Status: Ready", 
                                    font=('Arial', 12), 
                                    fg='#ffff00', bg='#1a1a1a')
        self.status_label.pack(side='left')
        
        self.time_label = tk.Label(status_frame, text="", 
                                  font=('Arial', 12), 
                                  fg='#00ff00', bg='#1a1a1a')
        self.time_label.pack(side='right')
        
        # Conversation area
        conv_frame = tk.Frame(main_frame, bg='#1a1a1a')
        conv_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        conv_label = tk.Label(conv_frame, text="Conversation Log", 
                             font=('Arial', 14, 'bold'), 
                             fg='#00ff00', bg='#1a1a1a')
        conv_label.pack(anchor='w', pady=(0, 10))
        
        self.conversation_text = scrolledtext.ScrolledText(
            conv_frame, 
            height=15, 
            bg='#2a2a2a', 
            fg='#00ff00', 
            font=('Consolas', 11),
            insertbackground='#00ff00',
            selectbackground='#003300'
        )
        self.conversation_text.pack(fill='both', expand=True)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#1a1a1a')
        control_frame.pack(fill='x', pady=(0, 20))
        
        # Voice control buttons
        self.listen_button = tk.Button(control_frame, text="🎤 Start Listening", 
                                      command=self.toggle_listening,
                                      bg='#2a2a2a', fg='#00ff00', 
                                      font=('Arial', 12),
                                      relief='raised', bd=2)
        self.listen_button.pack(side='left', padx=(0, 10))
        
        self.speak_button = tk.Button(control_frame, text="🔊 Test Voice", 
                                     command=self.test_voice,
                                     bg='#2a2a2a', fg='#00ff00', 
                                     font=('Arial', 12),
                                     relief='raised', bd=2)
        self.speak_button.pack(side='left', padx=(0, 10))
        
        self.clear_button = tk.Button(control_frame, text="🗑️ Clear Log", 
                                     command=self.clear_conversation,
                                     bg='#2a2a2a', fg='#ff0000', 
                                     font=('Arial', 12),
                                     relief='raised', bd=2)
        self.clear_button.pack(side='left')
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#1a1a1a')
        input_frame.pack(fill='x')
        
        input_label = tk.Label(input_frame, text="Text Command:", 
                              font=('Arial', 12), 
                              fg='#00ff00', bg='#1a1a1a')
        input_label.pack(anchor='w', pady=(0, 5))
        
        self.command_entry = tk.Entry(input_frame, 
                                     bg='#2a2a2a', fg='#00ff00', 
                                     font=('Arial', 11),
                                     insertbackground='#00ff00')
        self.command_entry.pack(fill='x', pady=(0, 10))
        self.command_entry.bind('<Return>', self.process_text_command)
        
        self.send_button = tk.Button(input_frame, text="Send Command", 
                                    command=self.process_text_command,
                                    bg='#2a2a2a', fg='#00ff00', 
                                    font=('Arial', 12),
                                    relief='raised', bd=2)
        self.send_button.pack(anchor='e')
        
        # Quick commands frame
        quick_frame = tk.Frame(main_frame, bg='#1a1a1a')
        quick_frame.pack(fill='x', pady=(20, 0))
        
        quick_label = tk.Label(quick_frame, text="Quick Commands:", 
                              font=('Arial', 12, 'bold'), 
                              fg='#00ff00', bg='#1a1a1a')
        quick_label.pack(anchor='w', pady=(0, 10))
        
        # Quick command buttons
        quick_buttons_frame = tk.Frame(quick_frame, bg='#1a1a1a')
        quick_buttons_frame.pack(fill='x')
        
        commands = [
            ("Time", "the time"),
            ("Weather", "weather"),
            ("News", "news"),
            ("Joke", "joke"),
            ("CPU", "cpu"),
            ("YouTube", "open youtube"),
            ("Google", "open google"),
            ("Wikipedia", "wikipedia artificial intelligence")
        ]
        
        for i, (label, command) in enumerate(commands):
            btn = tk.Button(quick_buttons_frame, text=label, 
                           command=lambda cmd=command: self.execute_quick_command(cmd),
                           bg='#2a2a2a', fg='#00ff00', 
                           font=('Arial', 10),
                           relief='raised', bd=1)
            btn.grid(row=i//4, column=i%4, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        for i in range(4):
            quick_buttons_frame.grid_columnconfigure(i, weight=1)
        
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
            self.listen_button.config(text="🔇 Stop Listening", bg='#3a2a2a')
            self.status_label.config(text="Status: Listening...", fg='#ff0000')
            
            # Start listening in separate thread
            threading.Thread(target=self.voice_listening_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.listen_button.config(text="🎤 Start Listening", bg='#2a2a2a')
            self.status_label.config(text="Status: Ready", fg='#ffff00')
    
    def voice_listening_loop(self):
        """Voice listening loop"""
        while self.is_listening:
            try:
                command = self.jarvis.listen()
                if command:
                    self.add_to_conversation("You", command)
                    response = self.jarvis.execute_command(command)
                    if response:
                        self.add_to_conversation("JARVIS", "Command executed successfully")
                    else:
                        self.add_to_conversation("JARVIS", "Goodbye Sir!")
                        self.is_listening = False
                        self.listen_button.config(text="🎤 Start Listening", bg='#2a2a2a')
                        self.status_label.config(text="Status: Ready", fg='#ffff00')
            except Exception as e:
                self.add_to_conversation("System", f"Voice error: {str(e)}")
                time.sleep(1)
    
    def test_voice(self):
        """Test voice output"""
        self.jarvis.speak("Voice test successful, Sir. I am ready to assist you.")
        self.add_to_conversation("JARVIS", "Voice test completed")
    
    def clear_conversation(self):
        """Clear conversation log"""
        self.conversation_text.delete(1.0, tk.END)
        self.conversation_history = []
        self.add_to_conversation("System", "Conversation log cleared")
    
    def process_text_command(self, event=None):
        """Process text command"""
        command = self.command_entry.get().strip()
        if command:
            self.add_to_conversation("You", command)
            response = self.jarvis.execute_command(command)
            if response:
                self.add_to_conversation("JARVIS", "Command executed successfully")
            else:
                self.add_to_conversation("JARVIS", "Goodbye Sir!")
            self.command_entry.delete(0, tk.END)
    
    def execute_quick_command(self, command):
        """Execute quick command"""
        self.add_to_conversation("You", command)
        response = self.jarvis.execute_command(command)
        if response:
            self.add_to_conversation("JARVIS", "Command executed successfully")
        else:
            self.add_to_conversation("JARVIS", "Goodbye Sir!")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    print("Starting JARVIS Simple GUI...")
    app = JARVISSimpleGUI()
    app.run()

if __name__ == "__main__":
    main()
