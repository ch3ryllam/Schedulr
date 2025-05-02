from .base import db
from .association import CoursePrereq
from .section import CourseSection


class Course(db.Model):
    """
    Cornell course.
    """

    __tablename__ = "course"
    number = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    credits = db.Column(db.Integer)

    sections = db.relationship("CourseSection", backref="course", lazy=True)
    prereqs = db.relationship(
        "CoursePrereq",
        foreign_keys="CoursePrereq.course_number",
        backref="course",
        lazy=True,
    )
    required_by = db.relationship(
        "CoursePrereq",
        foreign_keys="CoursePrereq.prereq_number",
        backref="prereq",
        lazy=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "number": self.number,
            "name": self.name,
            "description": self.description,
            "credits": self.credits,
            "sections": [s.serialize_no_course() for s in self.sections],
            "prereqs": [p.serialize_without_course() for p in self.prereqs],
            "required_by": [rb.serialize_without_prereq() for rb in self.required_by],
        }
