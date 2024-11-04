import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import base64
from config import ENVIRONMENTS, CURRENT_ENV


load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Add GitHub headers if token is available
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def send_discord_notification(test_message=False):
    config = ENVIRONMENTS[CURRENT_ENV]
    
    if test_message:
        data = {
            "content": "@here Test notification - Monitoring started! 🚀",
            "embeds": [{
                "title": f"🔔 {config['description']} Monitor Started!",
                "description": "Your job monitor is now running successfully!",
                "color": 5763719,
                "fields": [
                    {
                        "name": "Monitor Status",
                        "value": "✅ System is active and checking for new positions"
                    },
                    {
                        "name": "Environment",
                        "value": f"🌍 Running in {CURRENT_ENV.upper()} mode"
                    },
                    {
                        "name": "Check Interval",
                        "value": f"🕒 Checking every {config['check_interval']} seconds"
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
                "description": f"New positions have been added to the {config['description']} board!",
                "url": config['target_url'],
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

def get_latest_jobs():
    config = ENVIRONMENTS[CURRENT_ENV]
    try:
        print(f"🔍 Fetching from: {config['url']}")
        print(f"🔑 Using auth: {'Yes' if GITHUB_TOKEN else 'No'}")
        print(f"🔒 Repository is private: {'Yes' if CURRENT_ENV == 'test' else 'No'}")
        
        if not GITHUB_TOKEN and CURRENT_ENV == 'test':
            print("❌ Error: GitHub token is required for accessing private repositories")
            return None
            
        response = requests.get(config['url'], headers=headers)
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            content = base64.b64decode(response.json()['content']).decode('utf-8')
            
            # Find the table content
            table_start = content.find('| Company |')
            if table_start == -1:
                print("❌ Could not find job table in README")
                return None
            
            # Get the first few rows of the table
            lines = content[table_start:].split('\n')
            job_entries = []
            
            # Skip header and separator lines
            for line in lines[2:7]:  # Get first 5 job entries
                if '|' in line:
                    # Parse job entry
                    cells = [cell.strip() for cell in line.split('|')]
                    if len(cells) >= 5:
                        job_entries.append({
                            'company': cells[1],
                            'role': cells[2],
                            'location': cells[3]
                        })
            
            return job_entries
            
        print(f"❌ Failed to fetch README. Status code: {response.status_code}")
        if response.status_code == 403:
            print("Rate limit might be exceeded. Consider adding a GitHub token.")
        if response.status_code == 404:
            print("Repository or file not found. Please check the URL.")
        return None
    except Exception as e:
        print(f"❌ Error fetching README: {str(e)}")  # More detailed error
        return None

def monitor_repository():
    config = ENVIRONMENTS[CURRENT_ENV]
    print(f"🚀 Starting {config['description']} monitor...")
    print(f"🌍 Environment: {CURRENT_ENV.upper()}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if send_discord_notification(test_message=True):
        print("✅ Test message sent successfully!")
    else:
        print("❌ Failed to send test message. Please check your webhook URL.")
        return
    
    last_jobs = get_latest_jobs()
    if not last_jobs:
        print(f"❌ Failed to get initial job listings. Retrying in {config['check_interval']} seconds...")
    
    while True:
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n⏳ Checking for updates... [{current_time}]")
            
            current_jobs = get_latest_jobs()
            
            if current_jobs and last_jobs:
                # Check if any new jobs were added at the top
                new_jobs = []
                for job in current_jobs:
                    if job not in last_jobs:
                        new_jobs.append(job)
                
                if new_jobs:
                    print(f"🎉 {len(new_jobs)} new job(s) detected!")
                    if send_discord_notification():
                        last_jobs = current_jobs
                else:
                    print("📝 No new jobs found")
            
            print(f"💤 Waiting {config['check_interval']} seconds...")
            time.sleep(config['check_interval'])
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("🔄 Continuing monitoring...")
            time.sleep(config['check_interval'])

def test_parsing():
    print("\n🧪 Testing README parsing...")
    print(f"🌍 Current environment: {CURRENT_ENV}")  # Debug line
    
    # Test GitHub token
    if not GITHUB_TOKEN:
        print("⚠️ Warning: No GitHub token found in environment variables")
    
    jobs = get_latest_jobs()
    
    if not jobs:
        print("❌ Failed to fetch jobs")
        return False
    
    print("\n📋 First 5 jobs found:")
    print("-" * 80)
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['company']} | {job['role']} | {job['location']}")
    print("-" * 80)
    
    # Basic validation
    required_keys = ['company', 'role', 'location']
    for job in jobs:
        missing_keys = [key for key in required_keys if not job.get(key)]
        if missing_keys:
            print(f"❌ Job entry missing required fields: {missing_keys}")
            print(f"Problematic entry: {job}")
            return False
        
        # Check for empty values
        empty_fields = [key for key in required_keys if not job[key].strip()]
        if empty_fields:
            print(f"❌ Job entry has empty fields: {empty_fields}")
            print(f"Problematic entry: {job}")
            return False
    
    print("✅ All jobs parsed successfully!")
    print(f"📊 Total jobs parsed: {len(jobs)}")
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_parsing()
            sys.exit(0)
        elif sys.argv[1] in ENVIRONMENTS:
            CURRENT_ENV = sys.argv[1]
    
    print(f"🔧 Running in {CURRENT_ENV.upper()} mode")
    monitor_repository()
