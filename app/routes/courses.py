from flask import Blueprint
from app.models import Course, CourseSection, CoreClass
from ..utils import success_response, failure_response

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
def list_courses():
    """Return all CS courses in the catalog."""
    courses = Course.query.all()
    return success_response({"courses": [course.serialize() for course in courses]})


@courses_bp.route("/<int:number>/")
def get_course(number):
    """Get info about a single course."""
    number_str = f"CS {number}"
    course = Course.query.get(number_str)
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())


@courses_bp.route("/sections/")
def list_sections():
    """Return all CS course sections (Fall 2025)."""
    sections = CourseSection.query.all()
    return success_response({"sections": [section.serialize() for section in sections]})


@courses_bp.route("/sections/<int:section_id>/")
def get_section(section_id):
    """Return a single course section by its ID."""
    section = CourseSection.query.get(section_id)
    if section is None:
        return failure_response("Section not found", 404)
    return success_response(section.serialize())


@courses_bp.route("/core-sets/")
def get_core_courses():
    """
    Return the 7 core CS courses.
    """
    core_courses = [course.serialize() for course in CoreClass.query.all()]
    return success_response({"courses": core_courses})
