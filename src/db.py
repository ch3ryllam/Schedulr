from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CompletedCourse(db.Model):
    __tablename__ = "completed_course"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)


class CoursePrereq(db.Model):
    __tablename__ = "course_prereq"
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)
    prereq_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)


class CoreClass(db.Model):
    __tablename__ = "core_class"
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    graduation_term = db.Column(db.String, nullable=False)
    interests = db.Column(db.String)
    availability = db.Column(db.String)

    generated_schedules = db.relationship("GeneratedSchedule", backref="user")
    completed_courses = db.relationship("CompletedCourse", backref="user")


class Course(db.Model):
    __tablename__ = "course"
    number = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    credits = db.Column(db.Integer)

    sections = db.relationship("CourseSection", backref="course")


class CourseSection(db.Model):
    __tablename__ = "course_section"
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, db.ForeignKey("course.number"), nullable=False)
    section = db.Column(db.String, nullable=False)
    days = db.Column(db.String, nullable=False)
    start_min = db.Column(db.Integer, nullable=False)
    end_min = db.Column(db.Integer, nullable=False)

    schedule_sections = db.relationship("ScheduleSection", backref="section")


class GeneratedSchedule(db.Model):
    __tablename__ = "generated_schedule"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score = db.Column(db.Float)
    rationale = db.Column(db.String)

    sections = db.relationship("ScheduleSection", backref="schedule")


class ScheduleSection(db.Model):
    __tablename__ = "schedule_section"
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(
        db.Integer, db.ForeignKey("generated_schedule.id"), nullable=False
    )
    section_id = db.Column(
        db.Integer, db.ForeignKey("course_section.id"), nullable=False
    )
