from .base import db


class CompletedCourse(db.Model):
    """
    Association table to track courses a user has completed.
    """

    __tablename__ = "completed_course"
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    course_number = db.Column(
        db.String, db.ForeignKey("course.number"), primary_key=True, nullable=False
    )

    course = db.relationship("Course", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "course_number": self.course_number,
        }

    def serialize_without_user_id(self):
        return {
            "course_number": self.course_number,
        }


class CoursePrereq(db.Model):
    """
    Association table to track course prerequisites.
    """

    __tablename__ = "course_prereq"
    course_number = db.Column(
        db.String, db.ForeignKey("course.number"), primary_key=True, nullable=False
    )
    prereq_number = db.Column(
        db.String, db.ForeignKey("course.number"), primary_key=True, nullable=False
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "course_number": self.course_number,
            "prereq_number": self.prereq_number,
        }

    def serialize_without_course(self):
        return {"prereq_number": self.prereq_number}

    def serialize_without_prereq(self):
        return {"course_number": self.course_number}


class CoreClass(db.Model):
    """
    Table for core classes a student must take.
    """

    __tablename__ = "core_class"
    course_number = db.Column(
        db.String, db.ForeignKey("course.number"), nullable=False, primary_key=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {"course_number": self.course_number}
