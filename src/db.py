from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CompletedCourse(db.Model):
    """
    Association table to track courses a user has completed.
    """

    __tablename__ = "completed_course"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_number": self.course_number,
        }


class CoursePrereq(db.Model):
    """
    Association table to track course prerequisites.
    """

    __tablename__ = "course_prereq"
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)
    prereq_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)

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
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)

    def serialize(self):
        return {"id": self.id, "course_number": self.course_number}


class User(db.Model):
    """
    User of the chatbot.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    graduation_term = db.Column(db.String, nullable=False)
    interests = db.Column(db.String)
    availability = db.Column(db.String)

    generated_schedules = db.relationship("GeneratedSchedule", backref="user")
    completed_courses = db.relationship("CompletedCourse", backref="user")

    def serialize(self):
        return {
            "id": self.id,
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
    number = db.Column(db.String, primary_key=True)  # Example: "CS 3110"
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    credits = db.Column(db.Integer)

    sections = db.relationship("CourseSection", backref="course")

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
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)
    section = db.Column(db.String, nullable=False)  # Example: "LEC 001"
    days = db.Column(db.String, nullable=False)  # Example: "MWF"
    start_min = db.Column(db.Integer, nullable=False)
    end_min = db.Column(db.Integer, nullable=False)

    schedule_sections = db.relationship("ScheduleSection", backref="section")

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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score = db.Column(db.Float)
    rationale = db.Column(db.String)

    sections = db.relationship("ScheduleSection", backref="schedule")

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
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(
        db.Integer, db.ForeignKey("generated_schedule.id"), nullable=False
    )
    section_id = db.Column(
        db.Integer, db.ForeignKey("course_section.id"), nullable=False
    )

    def serialize(self):
        return {
            "id": self.id,
            "schedule_id": self.schedule_id,
            "section_id": self.section_id,
        }
