"""
Advanced Features for JARVIS
Calendar integration, email automation, web scraping, and more
"""

import os
import json
import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from config import Config

class AdvancedFeatures:
    def __init__(self):
        self.config = Config()
        self.calendar_events = []
        self.email_templates = self.load_email_templates()
        self.web_scraping_data = {}
        
    def load_email_templates(self):
        """Load email templates"""
        templates = {
            "meeting_request": """
            Subject: Meeting Request - {subject}
            
            Dear {recipient},
            
            I hope this email finds you well. I would like to schedule a meeting to discuss {topic}.
            
            Please let me know your availability for the following times:
            {suggested_times}
            
            Looking forward to hearing from you.
            
            Best regards,
            {sender_name}
            """,
            "follow_up": """
            Subject: Follow-up on {subject}
            
            Dear {recipient},
            
            I wanted to follow up on our previous discussion regarding {topic}.
            
            {follow_up_content}
            
            Please let me know if you have any questions.
            
            Best regards,
            {sender_name}
            """,
            "reminder": """
            Subject: Reminder: {subject}
            
            Dear {recipient},
            
            This is a friendly reminder about {reminder_content}.
            
            {additional_info}
            
            Best regards,
            {sender_name}
            """
        }
        return templates
    
    def calendar_integration(self, action, **kwargs):
        """Calendar integration functionality"""
        try:
            if action == "add_event":
                event = {
                    "title": kwargs.get("title", "New Event"),
                    "start_time": kwargs.get("start_time", datetime.now()),
                    "end_time": kwargs.get("end_time", datetime.now() + timedelta(hours=1)),
                    "description": kwargs.get("description", ""),
                    "location": kwargs.get("location", ""),
                    "reminder": kwargs.get("reminder", 15)  # minutes before
                }
                self.calendar_events.append(event)
                return f"Event '{event['title']}' added to calendar"
            
            elif action == "get_today_events":
                today = datetime.now().date()
                today_events = [e for e in self.calendar_events 
                              if e['start_time'].date() == today]
                if today_events:
                    events_text = "Today's events:\n"
                    for event in today_events:
                        events_text += f"- {event['title']} at {event['start_time'].strftime('%H:%M')}\n"
                    return events_text
                else:
                    return "No events scheduled for today"
            
            elif action == "get_upcoming_events":
                upcoming = [e for e in self.calendar_events 
                           if e['start_time'] > datetime.now()]
                if upcoming:
                    events_text = "Upcoming events:\n"
                    for event in upcoming[:5]:  # Next 5 events
                        events_text += f"- {event['title']} on {event['start_time'].strftime('%Y-%m-%d %H:%M')}\n"
                    return events_text
                else:
                    return "No upcoming events"
            
            elif action == "schedule_meeting":
                # Schedule a meeting with automatic email
                meeting_data = {
                    "title": kwargs.get("title", "Team Meeting"),
                    "participants": kwargs.get("participants", []),
                    "duration": kwargs.get("duration", 60),
                    "agenda": kwargs.get("agenda", "")
                }
                
                # Add to calendar
                self.calendar_integration("add_event", **meeting_data)
                
                # Send meeting invitations
                for participant in meeting_data["participants"]:
                    self.send_email(
                        to=participant,
                        subject=f"Meeting Invitation: {meeting_data['title']}",
                        body=self.email_templates["meeting_request"].format(
                            subject=meeting_data['title'],
                            recipient=participant,
                            topic=meeting_data['agenda'],
                            suggested_times="Please suggest your availability",
                            sender_name="JARVIS Assistant"
                        )
                    )
                
                return f"Meeting '{meeting_data['title']}' scheduled and invitations sent"
            
            else:
                return f"Unknown calendar action: {action}"
                
        except Exception as e:
            return f"Calendar error: {str(e)}"
    
    def email_automation(self, action, **kwargs):
        """Advanced email automation"""
        try:
            if action == "send_email":
                return self.send_email(
                    to=kwargs.get("to"),
                    subject=kwargs.get("subject", ""),
                    body=kwargs.get("body", ""),
                    attachments=kwargs.get("attachments", [])
                )
            
            elif action == "send_template":
                template_name = kwargs.get("template", "meeting_request")
                template_data = kwargs.get("template_data", {})
                
                if template_name in self.email_templates:
                    body = self.email_templates[template_name].format(**template_data)
                    return self.send_email(
                        to=kwargs.get("to"),
                        subject=template_data.get("subject", "Email from JARVIS"),
                        body=body
                    )
                else:
                    return f"Template '{template_name}' not found"
            
            elif action == "schedule_email":
                # Schedule email for later sending
                send_time = kwargs.get("send_time", datetime.now() + timedelta(minutes=1))
                email_data = {
                    "to": kwargs.get("to"),
                    "subject": kwargs.get("subject", ""),
                    "body": kwargs.get("body", ""),
                    "send_time": send_time
                }
                
                # Schedule the email
                schedule.every().day.at(send_time.strftime("%H:%M")).do(
                    self.send_email, **email_data
                )
                
                return f"Email scheduled for {send_time.strftime('%Y-%m-%d %H:%M')}"
            
            elif action == "email_summary":
                # Generate email summary (placeholder)
                return "Email summary feature coming soon"
            
            else:
                return f"Unknown email action: {action}"
                
        except Exception as e:
            return f"Email automation error: {str(e)}"
    
    def send_email(self, to, subject, body, attachments=None):
        """Send email using SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.EMAIL_USERNAME
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    with open(attachment, "rb") as f:
                        attachment_data = f.read()
                        attachment_part = MIMEText(attachment_data)
                        attachment_part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(attachment)}'
                        )
                        msg.attach(attachment_part)
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.config.EMAIL_USERNAME, self.config.EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(self.config.EMAIL_USERNAME, to, text)
            server.quit()
            
            return f"Email sent successfully to {to}"
            
        except Exception as e:
            return f"Email sending failed: {str(e)}"
    
    def web_scraping(self, action, **kwargs):
        """Advanced web scraping capabilities"""
        try:
            if action == "scrape_news":
                url = kwargs.get("url", "https://news.google.com")
                return self.scrape_news_headlines(url)
            
            elif action == "scrape_weather":
                location = kwargs.get("location", "New York")
                return self.scrape_weather_data(location)
            
            elif action == "scrape_stock":
                symbol = kwargs.get("symbol", "AAPL")
                return self.scrape_stock_data(symbol)
            
            elif action == "scrape_website":
                url = kwargs.get("url")
                selectors = kwargs.get("selectors", {})
                return self.scrape_custom_website(url, selectors)
            
            elif action == "monitor_price":
                url = kwargs.get("url")
                target_price = kwargs.get("target_price")
                return self.monitor_price_changes(url, target_price)
            
            else:
                return f"Unknown scraping action: {action}"
                
        except Exception as e:
            return f"Web scraping error: {str(e)}"
    
    def scrape_news_headlines(self, url):
        """Scrape news headlines"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = []
            for headline in soup.find_all(['h1', 'h2', 'h3'], limit=10):
                if headline.get_text().strip():
                    headlines.append(headline.get_text().strip())
            
            return f"Latest headlines: {'; '.join(headlines[:5])}"
            
        except Exception as e:
            return f"News scraping failed: {str(e)}"
    
    def scrape_weather_data(self, location):
        """Scrape weather data"""
        try:
            # Using a weather API instead of scraping
            api_key = self.config.WEATHER_API_KEY
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
            
            response = requests.get(url)
            data = response.json()
            
            if data['cod'] == 200:
                weather_info = f"""
                Weather in {location}:
                Temperature: {data['main']['temp']}°C
                Description: {data['weather'][0]['description']}
                Humidity: {data['main']['humidity']}%
                Wind Speed: {data['wind']['speed']} m/s
                """
                return weather_info
            else:
                return f"Weather data not available for {location}"
                
        except Exception as e:
            return f"Weather scraping failed: {str(e)}"
    
    def scrape_stock_data(self, symbol):
        """Scrape stock data"""
        try:
            # Using a financial API
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            response = requests.get(url)
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart']:
                result = data['chart']['result'][0]
                meta = result['meta']
                
                stock_info = f"""
                Stock: {symbol}
                Current Price: ${meta['regularMarketPrice']:.2f}
                Change: {meta['regularMarketChange']:.2f} ({meta['regularMarketChangePercent']:.2f}%)
                Volume: {meta['regularMarketVolume']:,}
                """
                return stock_info
            else:
                return f"Stock data not available for {symbol}"
                
        except Exception as e:
            return f"Stock scraping failed: {str(e)}"
    
    def scrape_custom_website(self, url, selectors):
        """Scrape custom website with specific selectors"""
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)
            
            scraped_data = {}
            for key, selector in selectors.items():
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    scraped_data[key] = element.text
                except:
                    scraped_data[key] = "Not found"
            
            driver.quit()
            return f"Scraped data: {json.dumps(scraped_data, indent=2)}"
            
        except Exception as e:
            return f"Custom scraping failed: {str(e)}"
    
    def monitor_price_changes(self, url, target_price):
        """Monitor price changes and alert when target is reached"""
        def price_monitor():
            while True:
                try:
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    driver.get(url)
                    
                    # Find price element (customize selector as needed)
                    price_element = driver.find_element(By.CSS_SELECTOR, ".price")
                    current_price = float(price_element.text.replace('$', '').replace(',', ''))
                    
                    if current_price <= target_price:
                        # Send notification
                        self.send_notification(
                            title="Price Alert",
                            message=f"Target price reached: ${current_price}"
                        )
                        break
                    
                    driver.quit()
                    time.sleep(300)  # Check every 5 minutes
                    
                except Exception as e:
                    print(f"Price monitoring error: {e}")
                    time.sleep(300)
        
        threading.Thread(target=price_monitor, daemon=True).start()
        return f"Price monitoring started for target: ${target_price}"
    
    def file_management_advanced(self, action, **kwargs):
        """Advanced file management"""
        try:
            if action == "organize_by_date":
                directory = kwargs.get("directory", os.path.expanduser("~/Downloads"))
                return self.organize_files_by_date(directory)
            
            elif action == "find_duplicates":
                directory = kwargs.get("directory", os.path.expanduser("~/Documents"))
                return self.find_duplicate_files(directory)
            
            elif action == "compress_files":
                files = kwargs.get("files", [])
                archive_name = kwargs.get("archive_name", "archive.zip")
                return self.compress_files(files, archive_name)
            
            elif action == "batch_rename":
                directory = kwargs.get("directory")
                pattern = kwargs.get("pattern", "file_{:03d}")
                return self.batch_rename_files(directory, pattern)
            
            else:
                return f"Unknown file management action: {action}"
                
        except Exception as e:
            return f"File management error: {str(e)}"
    
    def organize_files_by_date(self, directory):
        """Organize files by creation date"""
        try:
            files = os.listdir(directory)
            organized_count = 0
            
            for file in files:
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    creation_date = datetime.fromtimestamp(os.path.getctime(file_path))
                    date_folder = creation_date.strftime("%Y-%m-%d")
                    date_path = os.path.join(directory, date_folder)
                    
                    os.makedirs(date_path, exist_ok=True)
                    os.rename(file_path, os.path.join(date_path, file))
                    organized_count += 1
            
            return f"Organized {organized_count} files by date"
            
        except Exception as e:
            return f"Date organization failed: {str(e)}"
    
    def find_duplicate_files(self, directory):
        """Find duplicate files"""
        try:
            file_hashes = {}
            duplicates = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hash(f.read())
                        
                        if file_hash in file_hashes:
                            duplicates.append((file_hashes[file_hash], file_path))
                        else:
                            file_hashes[file_hash] = file_path
                    except:
                        continue
            
            if duplicates:
                return f"Found {len(duplicates)} duplicate files"
            else:
                return "No duplicate files found"
                
        except Exception as e:
            return f"Duplicate detection failed: {str(e)}"
    
    def compress_files(self, files, archive_name):
        """Compress files into archive"""
        try:
            import zipfile
            
            with zipfile.ZipFile(archive_name, 'w') as zipf:
                for file in files:
                    if os.path.exists(file):
                        zipf.write(file, os.path.basename(file))
            
            return f"Files compressed into {archive_name}"
            
        except Exception as e:
            return f"Compression failed: {str(e)}"
    
    def batch_rename_files(self, directory, pattern):
        """Batch rename files with pattern"""
        try:
            files = os.listdir(directory)
            renamed_count = 0
            
            for i, file in enumerate(files):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    file_ext = os.path.splitext(file)[1]
                    new_name = pattern.format(i + 1) + file_ext
                    new_path = os.path.join(directory, new_name)
                    os.rename(file_path, new_path)
                    renamed_count += 1
            
            return f"Renamed {renamed_count} files"
            
        except Exception as e:
            return f"Batch rename failed: {str(e)}"
    
    def send_notification(self, title, message):
        """Send desktop notification"""
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
            return "Notification sent"
        except Exception as e:
            return f"Notification failed: {str(e)}"
