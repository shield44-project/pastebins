"""
Configuration file for the Code Storage Website
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    CODES_DIRECTORY = os.environ.get('CODES_DIRECTORY', 'stored_codes')
    
    # Flask settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', '5000'))
    
    # Execution limits
    EXECUTION_TIMEOUT = 5  # seconds
    COMPILATION_TIMEOUT = 10  # seconds

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    def __init__(self):
        super().__init__()
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY must be set in production")
        self.SECRET_KEY = os.environ.get('SECRET_KEY')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
