# Job Alert Monitor

A Python script that monitors the SimplifyJobs New Grad Positions repository and sends Discord notifications when new jobs are posted.

## Features

- 🔍 Monitors GitHub repository for updates
- 🚨 Sends Discord notifications for new job postings
- ⏰ Checks every minute
- 🔔 Sends test message on startup

Run this for testing parsing on README.md file:
```
python monitor.py --test
```

Run this for testing or production:
```
python monitor.py
```