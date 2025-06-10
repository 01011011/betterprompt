"""
Database configuration and initialization for BetterPrompt application.

This module provides the SQLAlchemy database instance and configuration
for the Flask application with PostgreSQL backend.
"""

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app
import logging

# Initialize SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration settings."""
    
    @staticmethod
    def get_database_url():
        """Get database URL from environment variables."""
        # Priority: DATABASE_URL > individual components > defaults
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            return database_url
            
        # Construct from individual components
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        user = os.getenv('DB_USER', 'betterprompt_user')
        password = os.getenv('DB_PASSWORD', 'betterprompt_pass')
        database = os.getenv('DB_NAME', 'betterprompt_dev')
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    @staticmethod
    def get_redis_url():
        """Get Redis URL from environment variables."""
        redis_url = os.getenv('REDIS_URL')
        
        if redis_url:
            return redis_url
            
        # Construct from individual components
        host = os.getenv('REDIS_HOST', 'localhost')
        port = os.getenv('REDIS_PORT', '6379')
        db_num = os.getenv('REDIS_DB', '0')
        
        return f"redis://{host}:{port}/{db_num}"


def init_db(app):
    """
    Initialize database with Flask application.
    
    Args:
        app: Flask application instance
    """
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfig.get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True,
        'echo': app.config.get('SQLALCHEMY_ECHO', False)
    }
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    logger.info("Database initialized successfully")


def create_tables(app):
    """
    Create database tables.
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise


def check_db_connection():
    """
    Check database connection health.
    
    Returns:
        bool: True if connection is healthy, False otherwise
    """
    try:
        # Simple query to test connection
        db.session.execute(db.text('SELECT 1'))
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


def get_db_info():
    """
    Get database information for monitoring.
    
    Returns:
        dict: Database connection information
    """
    try:
        result = db.session.execute(db.text("""
            SELECT 
                version() as version,
                current_database() as database,
                current_user as user,
                inet_server_addr() as host,
                inet_server_port() as port
        """)).fetchone()
        
        return {
            'version': result.version if result else 'unknown',
            'database': result.database if result else 'unknown',
            'user': result.user if result else 'unknown',
            'host': result.host if result else 'unknown',
            'port': result.port if result else 'unknown',
            'url': DatabaseConfig.get_database_url().split('@')[1] if '@' in DatabaseConfig.get_database_url() else 'unknown'
        }
    except Exception as e:
        logger.error(f"Error getting database info: {e}")
        return {'error': str(e)}
