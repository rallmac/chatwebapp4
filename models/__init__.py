from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import your models here
from .user import User
from .message import Message
from .place import Place  # Add other models as needed
