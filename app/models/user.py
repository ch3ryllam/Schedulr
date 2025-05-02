from .base import db
from .association import CompletedCourse
from .schedule import GeneratedSchedule


class User(db.Model):
    """
    User of the chatbot.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    netid = db.Column(db.String, nullable=False)
    graduation_year = db.Column(db.String, nullable=False)
    interests = db.Column(db.String, nullable=True)
    availability = db.Column(db.String, nullable=True)

    completed_courses = db.relationship(
        "CompletedCourse", backref="user", cascade="all, delete-orphan"
    )
    generated_schedules = db.relationship(
        "GeneratedSchedule", backref="user", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "netid": self.netid,
            "graduation_year": self.graduation_year,
            "interests": self.interests,
            "availability": self.availability,
            "completed_courses": [
                c.serialize_without_user_id() for c in self.completed_courses
            ],
            "generated_schedules": [
                s.serialize_no_sections() for s in self.generated_schedules
            ],
        }
