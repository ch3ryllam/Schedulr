from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.model):
    """
    Model for courses.
    """
