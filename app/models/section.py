from .base import db


class CourseSection(db.Model):
    """
    Section of a course (like a lecture or discussion).
    """

    __tablename__ = "course_section"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)
    section = db.Column(db.String, nullable=False)
    days = db.Column(db.String, nullable=False)
    start_min = db.Column(db.Integer, nullable=True)
    end_min = db.Column(db.Integer, nullable=True)

    schedule_sections = db.relationship("ScheduleSection", backref="section")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "course_number": self.course_number,
            "section": self.section,
            "days": self.days,
            "start_min": self.start_min,
            "end_min": self.end_min,
        }

    def serialize_no_course(self):
        return {
            "id": self.id,
            "section": self.section,
            "days": self.days,
            "start_min": self.start_min,
            "end_min": self.end_min,
        }
