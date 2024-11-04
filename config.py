import os

# MONITOR_ENV is set to test in testing environment, but Heroku will have it set to 'prod'
CURRENT_ENV = os.getenv('MONITOR_ENV')

ENVIRONMENTS = {
    'test': {
        'url': "https://api.github.com/repos/jordanconklin/test/contents/README.md",
        'check_interval': 30,
        'target_url': "https://github.com/jordanconklin/test",
        'description': "Test Repository"
    },
    'prod': {
        'url': "https://api.github.com/repos/SimplifyJobs/New-Grad-Positions/contents/README.md",
        'check_interval': 60,
        'target_url': "https://github.com/SimplifyJobs/New-Grad-Positions",
        'description': "New Grad Positions"
    }
}
