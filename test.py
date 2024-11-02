import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Replace these with your test repository details
TEST_OWNER = "jordanconklin"
TEST_REPO = "test"

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {}
if GITHUB_TOKEN:
    headers['Authorization'] = f'token {GITHUB_TOKEN}'

def send_discord_notification(test_message=False):
    if test_message:
        data = {
            "content": "@here 🧪 Test Monitor Started!",
            "embeds": [{
                "title": "🔔 Test Monitor Active",
                "description": "Monitoring test repository for changes",
                "color": 5763719,
                "fields": [
                    {
                        "name": "Repository",
                        "value": f"📁 {TEST_OWNER}/{TEST_REPO}"
                    },
                    {
                        "name": "Check Interval",
                        "value": "🕒 Checking every 30 seconds"
                    }
                ],
                "footer": {
                    "text": f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }]
        }
    else:
        data = {
            "content": "@here 🧪 Test Change Detected!",
            "embeds": [{
                "title": "🔄 Repository Updated",
                "description": "A change was detected in the test repository!",
                "url": f"https://github.com/{TEST_OWNER}/{TEST_REPO}",
                "color": 3447003,
                "fields": [
                    {
                        "name": "Repository",
                        "value": f"📁 {TEST_OWNER}/{TEST_REPO}"
                    },
                    {
                        "name": "View Changes",
                        "value": f"🔗 [Click to view repository](https://github.com/{TEST_OWNER}/{TEST_REPO})"
                    }
                ],
                "footer": {
                    "text": f"Detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
    url = f"https://api.github.com/repos/{TEST_OWNER}/{TEST_REPO}/contents/README.md"
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

def monitor_test_repository():
    print("🧪 Starting Test Repository Monitor...")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Monitoring: {TEST_OWNER}/{TEST_REPO}")
    
    if send_discord_notification(test_message=True):
        print("✅ Test message sent successfully!")
    else:
        print("❌ Failed to send test message. Please check your webhook URL.")
        return
    
    last_sha = get_readme_content()
    if not last_sha:
        print("❌ Failed to get initial README content. Retrying...")
    
    while True:
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n⏳ Checking for updates... [{current_time}]")
            
            current_sha = get_readme_content()
            
            if current_sha and current_sha != last_sha:
                print("🎉 Change detected in test repository!")
                if send_discord_notification():
                    last_sha = current_sha
            else:
                print("📝 No changes detected")
            
            print("💤 Waiting 30 seconds...")
            time.sleep(30)  # Check every 30 seconds for testing
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("🔄 Continuing monitoring...")
            time.sleep(30)

if __name__ == "__main__":
    monitor_test_repository()