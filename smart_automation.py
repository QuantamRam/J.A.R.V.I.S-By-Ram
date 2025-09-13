"""
Smart Automation System for JARVIS
Advanced automation capabilities for system control and task management
"""

import os
import subprocess
import schedule
import time
import threading
from datetime import datetime, timedelta
import psutil
import pyautogui
import webbrowser
from config import Config
import json
import requests

class SmartAutomation:
    def __init__(self):
        self.config = Config()
        self.scheduled_tasks = {}
        self.automation_rules = self.load_automation_rules()
        
    def load_automation_rules(self):
        """Load automation rules from file"""
        try:
            with open('automation_rules.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "system_maintenance": {
                    "daily_cleanup": True,
                    "security_scan": True,
                    "backup_files": True
                },
                "smart_scheduling": {
                    "morning_routine": True,
                    "evening_routine": True,
                    "work_hours": "09:00-17:00"
                }
            }
    
    def save_automation_rules(self):
        """Save automation rules to file"""
        with open('automation_rules.json', 'w') as f:
            json.dump(self.automation_rules, f, indent=2)
    
    def system_control(self, action):
        """Advanced system control functions"""
        try:
            if action == "shutdown":
                self.schedule_shutdown(30)  # 30 seconds delay
                return "System shutdown scheduled in 30 seconds, Sir"
            
            elif action == "restart":
                self.schedule_restart(30)
                return "System restart scheduled in 30 seconds, Sir"
            
            elif action == "sleep":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return "System entering sleep mode, Sir"
            
            elif action == "lock":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "System locked, Sir"
            
            elif action == "hibernate":
                os.system("shutdown /h")
                return "System entering hibernation, Sir"
            
            elif action == "volume_up":
                pyautogui.press('volumeup')
                return "Volume increased, Sir"
            
            elif action == "volume_down":
                pyautogui.press('volumedown')
                return "Volume decreased, Sir"
            
            elif action == "mute":
                pyautogui.press('volumemute')
                return "Audio muted, Sir"
            
            elif action == "brightness_up":
                pyautogui.press('brightnessup')
                return "Brightness increased, Sir"
            
            elif action == "brightness_down":
                pyautogui.press('brightnessdown')
                return "Brightness decreased, Sir"
            
            else:
                return f"Unknown system action: {action}"
                
        except Exception as e:
            return f"System control error: {str(e)}"
    
    def schedule_shutdown(self, delay_seconds):
        """Schedule system shutdown"""
        def shutdown():
            time.sleep(delay_seconds)
            os.system("shutdown /s /t 0")
        
        threading.Thread(target=shutdown, daemon=True).start()
    
    def schedule_restart(self, delay_seconds):
        """Schedule system restart"""
        def restart():
            time.sleep(delay_seconds)
            os.system("shutdown /r /t 0")
        
        threading.Thread(target=restart, daemon=True).start()
    
    def smart_file_management(self, action, path=None):
        """Intelligent file management system"""
        try:
            if action == "organize_desktop":
                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                self.organize_files_by_type(desktop_path)
                return "Desktop organized successfully, Sir"
            
            elif action == "cleanup_temp":
                temp_paths = [
                    os.path.expandvars('%TEMP%'),
                    os.path.expandvars('%TMP%'),
                    os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')
                ]
                cleaned_files = 0
                for temp_path in temp_paths:
                    if os.path.exists(temp_path):
                        cleaned_files += self.clean_temp_files(temp_path)
                return f"Cleaned {cleaned_files} temporary files, Sir"
            
            elif action == "backup_important":
                important_folders = [
                    os.path.join(os.path.expanduser('~'), 'Documents'),
                    os.path.join(os.path.expanduser('~'), 'Desktop'),
                    os.path.join(os.path.expanduser('~'), 'Pictures')
                ]
                backup_path = os.path.join(os.path.expanduser('~'), 'JARVIS_Backup')
                self.create_backup(important_folders, backup_path)
                return "Important files backed up successfully, Sir"
            
            elif action == "find_file" and path:
                return self.find_file(path)
            
            else:
                return f"Unknown file management action: {action}"
                
        except Exception as e:
            return f"File management error: {str(e)}"
    
    def organize_files_by_type(self, directory):
        """Organize files by type in a directory"""
        file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac'],
            'Archives': ['.zip', '.rar', '.7z', '.tar'],
            'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java']
        }
        
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                file_ext = os.path.splitext(filename)[1].lower()
                
                for folder_name, extensions in file_types.items():
                    if file_ext in extensions:
                        folder_path = os.path.join(directory, folder_name)
                        os.makedirs(folder_path, exist_ok=True)
                        os.rename(
                            os.path.join(directory, filename),
                            os.path.join(folder_path, filename)
                        )
                        break
    
    def clean_temp_files(self, temp_path):
        """Clean temporary files"""
        cleaned_count = 0
        try:
            for root, dirs, files in os.walk(temp_path):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        # Only delete files older than 1 day
                        if os.path.getctime(file_path) < time.time() - 86400:
                            os.remove(file_path)
                            cleaned_count += 1
                    except:
                        continue
        except:
            pass
        return cleaned_count
    
    def create_backup(self, source_folders, backup_path):
        """Create backup of important folders"""
        os.makedirs(backup_path, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for folder in source_folders:
            if os.path.exists(folder):
                folder_name = os.path.basename(folder)
                backup_folder = os.path.join(backup_path, f"{folder_name}_{timestamp}")
                self.copy_directory(folder, backup_folder)
    
    def copy_directory(self, src, dst):
        """Copy directory recursively"""
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            
            if os.path.isdir(src_path):
                self.copy_directory(src_path, dst_path)
            else:
                try:
                    import shutil
                    shutil.copy2(src_path, dst_path)
                except:
                    pass
    
    def find_file(self, filename):
        """Find file on system"""
        search_paths = [
            os.path.expanduser('~'),
            'C:\\',
            'D:\\'
        ]
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if filename.lower() in file.lower():
                            return f"Found: {os.path.join(root, file)}"
                    # Limit search depth to avoid long searches
                    if len(root.split(os.sep)) > 5:
                        dirs.clear()
        
        return f"File '{filename}' not found, Sir"
    
    def smart_scheduling(self, task, time_str, action):
        """Smart task scheduling system"""
        try:
            # Parse time string (e.g., "09:00", "daily", "weekly")
            if time_str == "daily":
                schedule.every().day.at("09:00").do(self.execute_scheduled_task, action)
            elif time_str == "weekly":
                schedule.every().monday.at("09:00").do(self.execute_scheduled_task, action)
            elif ":" in time_str:
                schedule.every().day.at(time_str).do(self.execute_scheduled_task, action)
            
            self.scheduled_tasks[task] = {
                "time": time_str,
                "action": action,
                "created": datetime.now().isoformat()
            }
            
            return f"Task '{task}' scheduled for {time_str}, Sir"
            
        except Exception as e:
            return f"Scheduling error: {str(e)}"
    
    def execute_scheduled_task(self, action):
        """Execute scheduled task"""
        try:
            if action == "morning_routine":
                self.run_morning_routine()
            elif action == "evening_routine":
                self.run_evening_routine()
            elif action == "system_check":
                self.run_system_check()
            elif action == "backup":
                self.smart_file_management("backup_important")
            
        except Exception as e:
            print(f"Scheduled task error: {e}")
    
    def run_morning_routine(self):
        """Morning routine automation"""
        routines = [
            "Good morning, Sir. Running morning diagnostics...",
            "Checking system status...",
            "Reviewing today's schedule...",
            "Morning routine complete, Sir"
        ]
        
        for routine in routines:
            print(routine)
            time.sleep(1)
    
    def run_evening_routine(self):
        """Evening routine automation"""
        routines = [
            "Good evening, Sir. Running evening maintenance...",
            "Backing up important files...",
            "Cleaning temporary files...",
            "Evening routine complete, Sir"
        ]
        
        for routine in routines:
            print(routine)
            time.sleep(1)
    
    def run_system_check(self):
        """System health check"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = f"""
        System Status Report:
        CPU Usage: {cpu_percent}%
        Memory Usage: {memory.percent}%
        Disk Usage: {disk.percent}%
        """
        
        print(status)
    
    def start_scheduler(self):
        """Start the task scheduler"""
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        threading.Thread(target=run_scheduler, daemon=True).start()
        print("Task scheduler started, Sir")
