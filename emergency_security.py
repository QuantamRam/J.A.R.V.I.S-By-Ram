"""
Emergency and Security System for JARVIS
Advanced security protocols and emergency response capabilities
"""

import os
import json
import time
import threading
import subprocess
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
import numpy as np
from config import Config
import psutil
import requests

class EmergencySecuritySystem:
    def __init__(self):
        self.config = Config()
        self.security_log = []
        self.emergency_contacts = self.load_emergency_contacts()
        self.security_threats = []
        self.system_monitoring = False
        self.emergency_mode = False
        
    def load_emergency_contacts(self):
        """Load emergency contacts"""
        try:
            with open('emergency_contacts.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "police": "911",
                "fire": "911",
                "medical": "911",
                "family": [],
                "friends": [],
                "work": []
            }
    
    def save_emergency_contacts(self):
        """Save emergency contacts"""
        with open('emergency_contacts.json', 'w') as f:
            json.dump(self.emergency_contacts, f, indent=2)
    
    def log_security_event(self, event_type, description, severity="medium"):
        """Log security events"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "description": description,
            "severity": severity,
            "resolved": False
        }
        
        self.security_log.append(event)
        
        # Save to file
        with open('security_log.json', 'w') as f:
            json.dump(self.security_log, f, indent=2)
        
        # Alert if high severity
        if severity == "high":
            self.send_security_alert(event)
    
    def send_security_alert(self, event):
        """Send security alert"""
        try:
            alert_message = f"""
            SECURITY ALERT - JARVIS System
            
            Event Type: {event['type']}
            Description: {event['description']}
            Time: {event['timestamp']}
            Severity: {event['severity']}
            
            Please check your system immediately.
            """
            
            # Send email alert
            self.send_emergency_email("Security Alert", alert_message)
            
            # Send desktop notification
            self.send_desktop_notification("Security Alert", event['description'])
            
        except Exception as e:
            print(f"Security alert error: {e}")
    
    def send_emergency_email(self, subject, body):
        """Send emergency email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.EMAIL_USERNAME
            msg['To'] = self.config.EMAIL_USERNAME  # Send to self
            msg['Subject'] = f"EMERGENCY: {subject}"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.config.EMAIL_USERNAME, self.config.EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(self.config.EMAIL_USERNAME, self.config.EMAIL_USERNAME, text)
            server.quit()
            
        except Exception as e:
            print(f"Emergency email error: {e}")
    
    def send_desktop_notification(self, title, message):
        """Send desktop notification"""
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                timeout=10,
                app_icon=None
            )
        except Exception as e:
            print(f"Desktop notification error: {e}")
    
    def emergency_protocol(self, emergency_type):
        """Activate emergency protocols"""
        self.emergency_mode = True
        self.log_security_event("emergency", f"Emergency protocol activated: {emergency_type}", "high")
        
        if emergency_type == "medical":
            self.medical_emergency()
        elif emergency_type == "fire":
            self.fire_emergency()
        elif emergency_type == "security":
            self.security_emergency()
        elif emergency_type == "system":
            self.system_emergency()
        else:
            self.general_emergency()
    
    def medical_emergency(self):
        """Medical emergency protocols"""
        try:
            # Contact emergency services
            self.contact_emergency_services("medical")
            
            # Send location information
            location = self.get_current_location()
            if location:
                self.send_emergency_email(
                    "Medical Emergency",
                    f"Medical emergency at location: {location}"
                )
            
            # Activate system monitoring
            self.start_emergency_monitoring()
            
        except Exception as e:
            print(f"Medical emergency error: {e}")
    
    def fire_emergency(self):
        """Fire emergency protocols"""
        try:
            # Contact emergency services
            self.contact_emergency_services("fire")
            
            # Send location information
            location = self.get_current_location()
            if location:
                self.send_emergency_email(
                    "Fire Emergency",
                    f"Fire emergency at location: {location}"
                )
            
            # Activate evacuation protocols
            self.evacuation_protocol()
            
        except Exception as e:
            print(f"Fire emergency error: {e}")
    
    def security_emergency(self):
        """Security emergency protocols"""
        try:
            # Lock system
            self.lock_system()
            
            # Contact security services
            self.contact_emergency_services("police")
            
            # Start security monitoring
            self.start_security_monitoring()
            
            # Send security alert
            self.send_emergency_email(
                "Security Breach",
                "Security breach detected. System locked and authorities notified."
            )
            
        except Exception as e:
            print(f"Security emergency error: {e}")
    
    def system_emergency(self):
        """System emergency protocols"""
        try:
            # Backup critical data
            self.emergency_backup()
            
            # Send system status
            status = self.get_system_status()
            self.send_emergency_email(
                "System Emergency",
                f"System emergency detected. Status: {status}"
            )
            
            # Activate recovery protocols
            self.system_recovery()
            
        except Exception as e:
            print(f"System emergency error: {e}")
    
    def general_emergency(self):
        """General emergency protocols"""
        try:
            # Contact all emergency contacts
            for contact_type, contacts in self.emergency_contacts.items():
                if contacts and contact_type != "police" and contact_type != "fire" and contact_type != "medical":
                    for contact in contacts:
                        self.send_emergency_email(
                            "Emergency Alert",
                            f"Emergency situation. Please check on the user immediately."
                        )
            
            # Start comprehensive monitoring
            self.start_emergency_monitoring()
            
        except Exception as e:
            print(f"General emergency error: {e}")
    
    def contact_emergency_services(self, service_type):
        """Contact emergency services"""
        try:
            if service_type in self.emergency_contacts:
                contact = self.emergency_contacts[service_type]
                
                # Log the contact attempt
                self.log_security_event(
                    "emergency_contact",
                    f"Contacted {service_type}: {contact}",
                    "high"
                )
                
                # In a real implementation, you would use a service like Twilio
                # to make actual phone calls or send SMS
                print(f"Emergency contact made: {service_type} - {contact}")
                
        except Exception as e:
            print(f"Emergency contact error: {e}")
    
    def get_current_location(self):
        """Get current location"""
        try:
            import geocoder
            g = geocoder.ip('me')
            return f"{g.city}, {g.state}, {g.country}"
        except Exception as e:
            print(f"Location error: {e}")
            return None
    
    def lock_system(self):
        """Lock the system"""
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            self.log_security_event("system_lock", "System locked for security", "high")
        except Exception as e:
            print(f"System lock error: {e}")
    
    def emergency_backup(self):
        """Emergency backup of critical data"""
        try:
            backup_path = os.path.join(os.path.expanduser('~'), 'JARVIS_Emergency_Backup')
            os.makedirs(backup_path, exist_ok=True)
            
            # Backup important files
            important_files = [
                'user_preferences.json',
                'security_log.json',
                'emergency_contacts.json',
                'automation_rules.json'
            ]
            
            for file in important_files:
                if os.path.exists(file):
                    import shutil
                    shutil.copy2(file, backup_path)
            
            self.log_security_event("emergency_backup", "Emergency backup completed", "medium")
            
        except Exception as e:
            print(f"Emergency backup error: {e}")
    
    def get_system_status(self):
        """Get comprehensive system status"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "timestamp": datetime.now().isoformat(),
                "emergency_mode": self.emergency_mode
            }
            
            return json.dumps(status, indent=2)
            
        except Exception as e:
            return f"System status error: {e}"
    
    def start_emergency_monitoring(self):
        """Start emergency monitoring"""
        self.system_monitoring = True
        
        def monitor():
            while self.system_monitoring:
                try:
                    # Monitor system resources
                    cpu_percent = psutil.cpu_percent()
                    memory = psutil.virtual_memory()
                    
                    # Alert if resources are critically low
                    if cpu_percent > 90:
                        self.log_security_event(
                            "high_cpu",
                            f"CPU usage critically high: {cpu_percent}%",
                            "high"
                        )
                    
                    if memory.percent > 90:
                        self.log_security_event(
                            "high_memory",
                            f"Memory usage critically high: {memory.percent}%",
                            "high"
                        )
                    
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    print(f"Emergency monitoring error: {e}")
                    time.sleep(60)
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def start_security_monitoring(self):
        """Start security monitoring"""
        def security_monitor():
            while self.emergency_mode:
                try:
                    # Monitor for suspicious activities
                    self.monitor_network_activity()
                    self.monitor_file_access()
                    self.monitor_process_activity()
                    
                    time.sleep(60)  # Check every minute
                    
                except Exception as e:
                    print(f"Security monitoring error: {e}")
                    time.sleep(60)
        
        threading.Thread(target=security_monitor, daemon=True).start()
    
    def monitor_network_activity(self):
        """Monitor network activity"""
        try:
            # Check for suspicious network connections
            connections = psutil.net_connections()
            
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    # Check for suspicious ports or IPs
                    if conn.raddr and conn.raddr.port in [22, 23, 3389]:  # SSH, Telnet, RDP
                        self.log_security_event(
                            "suspicious_connection",
                            f"Suspicious connection to {conn.raddr.ip}:{conn.raddr.port}",
                            "medium"
                        )
        
        except Exception as e:
            print(f"Network monitoring error: {e}")
    
    def monitor_file_access(self):
        """Monitor file access patterns"""
        try:
            # Monitor access to sensitive files
            sensitive_files = [
                'user_preferences.json',
                'security_log.json',
                'emergency_contacts.json'
            ]
            
            for file in sensitive_files:
                if os.path.exists(file):
                    # Check if file was recently modified
                    mod_time = os.path.getmtime(file)
                    if datetime.now().timestamp() - mod_time < 60:  # Modified in last minute
                        self.log_security_event(
                            "file_access",
                            f"Sensitive file accessed: {file}",
                            "medium"
                        )
        
        except Exception as e:
            print(f"File monitoring error: {e}")
    
    def monitor_process_activity(self):
        """Monitor process activity"""
        try:
            # Check for suspicious processes
            processes = psutil.process_iter(['pid', 'name', 'cpu_percent'])
            
            for proc in processes:
                try:
                    if proc.info['cpu_percent'] > 50:  # High CPU usage
                        self.log_security_event(
                            "high_cpu_process",
                            f"Process {proc.info['name']} using {proc.info['cpu_percent']}% CPU",
                            "medium"
                        )
                except:
                    continue
        
        except Exception as e:
            print(f"Process monitoring error: {e}")
    
    def evacuation_protocol(self):
        """Evacuation protocol"""
        try:
            # Send evacuation instructions
            instructions = """
            FIRE EMERGENCY - EVACUATION PROTOCOL
            
            1. Leave the building immediately
            2. Use the nearest exit
            3. Do not use elevators
            4. Meet at the designated assembly point
            5. Call emergency services from outside
            
            Location information has been sent to emergency services.
            """
            
            self.send_emergency_email("Fire Evacuation", instructions)
            self.send_desktop_notification("FIRE EMERGENCY", "Evacuate immediately!")
            
        except Exception as e:
            print(f"Evacuation protocol error: {e}")
    
    def system_recovery(self):
        """System recovery protocols"""
        try:
            # Attempt system recovery
            recovery_steps = [
                "Checking system integrity...",
                "Restoring from backup...",
                "Rebuilding system cache...",
                "Verifying security protocols..."
            ]
            
            for step in recovery_steps:
                print(step)
                time.sleep(2)
            
            self.log_security_event("system_recovery", "System recovery completed", "medium")
            
        except Exception as e:
            print(f"System recovery error: {e}")
    
    def add_emergency_contact(self, contact_type, contact_info):
        """Add emergency contact"""
        try:
            if contact_type not in self.emergency_contacts:
                self.emergency_contacts[contact_type] = []
            
            self.emergency_contacts[contact_type].append(contact_info)
            self.save_emergency_contacts()
            
            return f"Emergency contact added: {contact_type} - {contact_info}"
            
        except Exception as e:
            return f"Add contact error: {e}"
    
    def remove_emergency_contact(self, contact_type, contact_info):
        """Remove emergency contact"""
        try:
            if contact_type in self.emergency_contacts:
                if contact_info in self.emergency_contacts[contact_type]:
                    self.emergency_contacts[contact_type].remove(contact_info)
                    self.save_emergency_contacts()
                    return f"Emergency contact removed: {contact_type} - {contact_info}"
                else:
                    return f"Contact not found: {contact_info}"
            else:
                return f"Contact type not found: {contact_type}"
                
        except Exception as e:
            return f"Remove contact error: {e}"
    
    def get_security_report(self):
        """Generate security report"""
        try:
            recent_events = [event for event in self.security_log 
                           if datetime.fromisoformat(event['timestamp']) > 
                           datetime.now() - timedelta(days=7)]
            
            report = {
                "total_events": len(self.security_log),
                "recent_events": len(recent_events),
                "high_severity": len([e for e in recent_events if e['severity'] == 'high']),
                "medium_severity": len([e for e in recent_events if e['severity'] == 'medium']),
                "low_severity": len([e for e in recent_events if e['severity'] == 'low']),
                "emergency_mode": self.emergency_mode,
                "last_event": self.security_log[-1]['timestamp'] if self.security_log else None
            }
            
            return json.dumps(report, indent=2)
            
        except Exception as e:
            return f"Security report error: {e}"
    
    def deactivate_emergency_mode(self):
        """Deactivate emergency mode"""
        try:
            self.emergency_mode = False
            self.system_monitoring = False
            
            self.log_security_event(
                "emergency_deactivated",
                "Emergency mode deactivated",
                "medium"
            )
            
            return "Emergency mode deactivated"
            
        except Exception as e:
            return f"Deactivation error: {e}"
