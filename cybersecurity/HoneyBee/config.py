import os
from werkzeug.security import generate_password_hash

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    LOG_DIR = 'logs'
    ARCHIVE_DIR = 'archives'
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Authentication
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'password'
    ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)
    
    # Alert settings
    ALERT_METHODS = ['email', 'slack', 'telegram']
    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    
    # Whitelist
    IP_WHITELIST = set()
    
    # Services
    SERVICES = {
        'SSH': 22,
        'FTP': 21,
        'HTTP': 80,
        'TELNET': 23,
        'MYSQL': 3306
    }