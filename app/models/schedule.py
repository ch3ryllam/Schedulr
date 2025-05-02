from .base import db
from .section import CourseSection


class GeneratedSchedule(db.Model):
    """
    A generated schedule suggestion for a user.
    """

    __tablename__ = "generated_schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # score = db.Column(db.Float)
    rationale = db.Column(db.String)

    schedule_sections = db.relationship(
        "ScheduleSection", backref="schedule", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            # "score": self.score,
            "rationale": self.rationale,
            "sections": [s.section.serialize() for s in self.schedule_sections],
        }

    def serialize_no_sections(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "rationale": self.rationale,
            # "score": self.score,
        }


class ScheduleSection(db.Model):
    """
    Maps a generated schedule to a set of course sections.
    """

    __tablename__ = "schedule_section"
    schedule_id = db.Column(
        db.Integer,
        db.ForeignKey("generated_schedule.id"),
        nullable=False,
        primary_key=True,
    )
    section_id = db.Column(
        db.Integer, db.ForeignKey("course_section.id"), nullable=False, primary_key=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "schedule_id": self.schedule_id,
            "section_id": self.section_id,
        }
