"""
Logger module for the arXiv email to Notion system.
Provides consistent logging functionality across the application.
"""
import os
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Define log levels dictionary for easier reference
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class Logger:
    """Custom logger class for the application"""
    
    def __init__(self, name='arxiv_email_monitor'):
        """
        Initialize the logger with the given name
        
        Args:
            name (str): The name of the logger
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Capture all levels, filtering happens at handler level
        self.logger.propagate = False  # Prevent duplicate logs
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        Path(log_dir).mkdir(exist_ok=True)
        
        # Log file path with timestamp for daily logs
        timestamp = datetime.now().strftime("%Y-%m-%d")
        self.log_file = os.path.join(log_dir, f'arxiv_monitor_{timestamp}.log')
        
        # Check if handlers already exist to avoid duplicates
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up console and file handlers with formatters"""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(LOG_LEVELS.get(os.getenv('CONSOLE_LOG_LEVEL', 'INFO')))
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        
        # File handler (rotating, max 10MB, keep 10 backup files)
        file_handler = RotatingFileHandler(
            self.log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(LOG_LEVELS.get(os.getenv('FILE_LOG_LEVEL', 'DEBUG')))
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
        file_handler.setFormatter(file_format)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    def exception(self, message):
        """Log exception message with traceback"""
        self.logger.exception(message)

# Create a default logger instance for import
logger = Logger().logger
