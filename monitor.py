import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Store webhook URL in .env file for security
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_discord_notification(test_message=False):
    if test_message:
        data = {
            "embeds": [{
                "title": "🔔 Job Monitor Started!",
                "description": "Test message - Your job monitor is now running successfully!",
                "color": 5763719,  # Green color
                "fields": [
                    {
                        "name": "Monitor Status",
                        "value": "✅ System is active and checking for new positions"
                    },
                    {
                        "name": "Check Interval",
                        "value": "🕒 Checking every 5 minutes"
                    }
                ],
                "footer": {
                    "text": f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }]
        }
    else:
        data = {
            "embeds": [{
                "title": "🚨 New Job Alert!",
                "description": "New positions have been added to the New Grad job board!",
                "url": "https://github.com/SimplifyJobs/New-Grad-Positions",
                "color": 3447003,  # Blue color
                "fields": [
                    {
                        "name": "Quick Links",
                        "value": "🔗 [View All Positions](https://github.com/SimplifyJobs/New-Grad-Positions)\n📱 [Simplify Job Search](https://simplify.jobs/)"
                    }
                ],
                "footer": {
                    "text": f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }]
        }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:  # Discord returns 204 on success
            print(f"✅ Discord notification sent! [{datetime.now().strftime('%H:%M:%S')}]")
            return True
        else:
            print(f"❌ Failed to send notification. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending Discord notification: {e}")
        return False

def get_readme_content():
    url = "https://api.github.com/repos/SimplifyJobs/New-Grad-Positions/contents/README.md"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['sha']
        print(f"❌ Failed to fetch README. Status code: {response.status_code}")
        return None
    except Exception as e:
        print(f"❌ Error fetching README: {e}")
        return None

def monitor_repository():
    print("🚀 Starting New Grad Positions monitor...")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Send test message on startup
    if send_discord_notification(test_message=True):
        print("✅ Test message sent successfully!")
    else:
        print("❌ Failed to send test message. Please check your webhook URL.")
        return
    
    last_sha = get_readme_content()
    if not last_sha:
        print("❌ Failed to get initial README content. Retrying in 5 minutes...")
    
    while True:
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n⏳ Checking for updates... [{current_time}]")
            
            current_sha = get_readme_content()
            
            if current_sha and current_sha != last_sha:
                print("🎉 New update detected!")
                if send_discord_notification():
                    last_sha = current_sha
            else:
                print("📝 No new updates found")
            
            print("💤 Waiting 5 minutes before next check...")
            time.sleep(300)  # 5 minutes
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("🔄 Continuing monitoring...")
            time.sleep(300)

if __name__ == "__main__":
    monitor_repository()