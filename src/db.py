from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CompletedCourse(db.Model):
    """
    Association table to track courses a user has completed.
    """

    __tablename__ = "completed_course"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), primary_key=True, nullable=False)

    course = db.relationship("Course", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "course_number": self.course_number,
        }


class CoursePrereq(db.Model):
    """
    Association table to track course prerequisites.
    """

    __tablename__ = "course_prereq"
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), primary_key=True, nullable=False)
    prereq_number = db.Column(db.String, db.ForeignKey("course.number"), primary_key=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "course_number": self.course_number,
            "prereq_number": self.prereq_number,
        }


class CoreClass(db.Model):
    """
    Table for core classes a student must take.
    """

    __tablename__ = "core_class"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_numbers = db.Column(db.ARRAY(db.Integer), db.ForeignKey("course.number"), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {"id": self.id, "course_number": self.course_numbers}


class User(db.Model):
    """
    User of the chatbot.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    netid = db.Column(db.String, unique=True, nullable=False)
    graduation_term = db.Column(db.String, nullable=False)
    interests = db.Column(db.ARRAY(db.String))

    #168 char string with 0s and 1s representing availability. 
    #If the 1st char is 1 that means someone is free on monday 12 am - 1 am, etc.
    availability = db.Column(db.String, nullable=False)

    generated_schedules = db.relationship("GeneratedSchedule", backref="user", lazy=True)
    completed_courses = db.relationship("CompletedCourse", backref="user", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "netid": self.netid,
            "graduation_term": self.graduation_term,
            "interests": self.interests,
            "availability": self.availability,
            "completed_courses": [c.serialize() for c in self.completed_courses],
            "generated_schedules": [
                s.serialize_no_sections() for s in self.generated_schedules
            ],
        }


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
    prereqs = db.relationship("CoursePrereq", foreign_keys="CoursePrereq.course_number", backref="course", lazy=True)
    required_by = db.relationship("CoursePrereq", foreign_keys="CoursePrereq.prereq_number", backref="prereq", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "number": self.number,
            "name": self.name,
            "description": self.description,
            "credits": self.credits,
            "sections": [s.serialize_no_course() for s in self.sections],
        }


class CourseSection(db.Model):
    """
    Section of a course (like a lecture or discussion).
    """

    __tablename__ = "course_section"
    id = db.Column(db.Integer, primary_key=True, autoincrements=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)
    section = db.Column(db.String, nullable=False)
    days = db.Column(db.String, nullable=False)
    start_min = db.Column(db.Integer, nullable=False)
    end_min = db.Column(db.Integer, nullable=False)

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


class GeneratedSchedule(db.Model):
    """
    A generated schedule suggestion for a user.
    """

    __tablename__ = "generated_schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score = db.Column(db.Float)
    rationale = db.Column(db.String)

    sections = db.relationship("ScheduleSection", backref="schedule", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "score": self.score,
            "rationale": self.rationale,
            "sections": [s.serialize() for s in self.sections],
        }

    def serialize_no_sections(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "score": self.score,
            "rationale": self.rationale,
        }


class ScheduleSection(db.Model):
    """
    Maps a generated schedule to a set of course sections.
    """

    __tablename__ = "schedule_section"
    schedule_id = db.Column(
        db.Integer, db.ForeignKey("generated_schedule.id"), nullable=False, primary_key=True
    )
    section_id = db.Column(
        db.Integer, db.ForeignKey("course_section.id"), nullable=False, primary_key=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "schedule_id": self.schedule_id,
            "section_id": self.section_id,
        }
