import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Add GitHub headers if token is available
headers = {}
if GITHUB_TOKEN:
    headers['Authorization'] = f'token {GITHUB_TOKEN}'

def send_discord_notification(test_message=False):
    if test_message:
        data = {
            "content": "@here Test notification - Monitoring started! 🚀",
            "embeds": [{
                "title": "🔔 Job Monitor Started!",
                "description": "Your job monitor is now running successfully!",
                "color": 5763719,
                "fields": [
                    {
                        "name": "Monitor Status",
                        "value": "✅ System is active and checking for new positions"
                    },
                    {
                        "name": "Check Interval",
                        "value": "🕒 Checking every minute"  # Updated interval
                    }
                ],
                "footer": {
                    "text": f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }]
        }
    else:
        data = {
            "content": "@here New jobs posted! 🚨",
            "embeds": [{
                "title": "🚨 New Job Alert!",
                "description": "New positions have been added to the New Grad job board!",
                "url": "https://github.com/SimplifyJobs/New-Grad-Positions",
                "color": 3447003,
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
        if response.status_code == 204:
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
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['sha']
        print(f"❌ Failed to fetch README. Status code: {response.status_code}")
        if response.status_code == 403:
            print("Rate limit might be exceeded. Consider adding a GitHub token.")
        return None
    except Exception as e:
        print(f"❌ Error fetching README: {e}")
        return None

def monitor_repository():
    print("🚀 Starting New Grad Positions monitor...")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if send_discord_notification(test_message=True):
        print("✅ Test message sent successfully!")
    else:
        print("❌ Failed to send test message. Please check your webhook URL.")
        return
    
    last_sha = get_readme_content()
    if not last_sha:
        print("❌ Failed to get initial README content. Retrying in 1 minute...")
    
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
            
            print("💤 Waiting 1 minute before next check...")
            time.sleep(60)  # 1 minute
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("🔄 Continuing monitoring...")
            time.sleep(60)

if __name__ == "__main__":
    monitor_repository()


'''
git add .
git commit -m "test commit"
git push heroku main

'''