from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.flaskModel import Story, Page, Choice

__all__ = ['db', 'Story', 'Page', 'Choice']