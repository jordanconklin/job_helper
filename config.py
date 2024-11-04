# Create a new file for configuration
ENVIRONMENTS = {
    'test': {
        'url': "https://api.github.com/repos/jordanconklin/test/contents/README.md",
        'check_interval': 20,  # 20 seconds for testing
        'target_url': "https://github.com/jordanconklin/test",
        'description': "Test Repository"
    },
    'prod': {
        'url': "https://api.github.com/repos/SimplifyJobs/New-Grad-Positions/contents/README.md",
        'check_interval': 60,  # 1 minute for production
        'target_url': "https://github.com/SimplifyJobs/New-Grad-Positions",
        'description': "New Grad Positions"
    }
}

# Set this to 'test' or 'prod'
CURRENT_ENV = 'test'