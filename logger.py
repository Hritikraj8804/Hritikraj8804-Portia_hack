#!/usr/bin/env python3
"""
Centralized logging system for DevOps AI Assistant
Provides structured logging with different levels and file rotation
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import json

class DevOpsLogger:
    def __init__(self, name="devops_assistant", log_dir="logs"):
        self.name = name
        self.log_dir = log_dir
        
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup file and console handlers"""
        
        # File handler with rotation (10MB max, keep 5 files)
        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message, **kwargs):
        """Log info message with optional context"""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def error(self, message, **kwargs):
        """Log error message with optional context"""
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def warning(self, message, **kwargs):
        """Log warning message with optional context"""
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def debug(self, message, **kwargs):
        """Log debug message with optional context"""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def _log_with_context(self, level, message, **kwargs):
        """Log message with additional context"""
        if kwargs:
            context = json.dumps(kwargs, default=str)
            full_message = f"{message} | Context: {context}"
        else:
            full_message = message
        
        self.logger.log(level, full_message)
    
    def log_api_call(self, endpoint, method="GET", status_code=None, duration=None):
        """Log API call details"""
        self.info(
            f"API Call: {method} {endpoint}",
            status_code=status_code,
            duration_ms=duration,
            timestamp=datetime.now().isoformat()
        )
    
    def log_pipeline_action(self, pipeline_id, action, status, user=None):
        """Log pipeline action"""
        self.info(
            f"Pipeline Action: {action} on {pipeline_id}",
            pipeline_id=pipeline_id,
            action=action,
            status=status,
            user=user,
            timestamp=datetime.now().isoformat()
        )
    
    def log_error_with_traceback(self, message, exception):
        """Log error with full traceback"""
        import traceback
        self.error(
            f"{message}: {str(exception)}",
            traceback=traceback.format_exc(),
            exception_type=type(exception).__name__
        )

# Global logger instances
app_logger = DevOpsLogger("app")
api_logger = DevOpsLogger("api")
frontend_logger = DevOpsLogger("frontend")

# Convenience functions
def log_info(message, **kwargs):
    app_logger.info(message, **kwargs)

def log_error(message, **kwargs):
    app_logger.error(message, **kwargs)

def log_warning(message, **kwargs):
    app_logger.warning(message, **kwargs)

def log_debug(message, **kwargs):
    app_logger.debug(message, **kwargs)