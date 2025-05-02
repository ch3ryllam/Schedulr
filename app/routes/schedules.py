import json
import re
from flask import Blueprint, request
from ..db import (
    db,
    User,
    GeneratedSchedule,
    ScheduleSection,
    Course,
    CourseSection,
    CoreClass,
    CoursePrereq,
)
from ..utils import success_response, failure_response
from ..gpt import gpt_rank_courses

schedules_bp = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedules_bp.route("/<int:user_id>/")
def list_schedules(user_id):
    """List all generated schedules for a user."""
    user = User.query.get(user_id)
    if user is None:
        return failure_response("User not found")

    schedules = [s.serialize() for s in user.generated_schedules]
    return success_response({"schedules": schedules})


@schedules_bp.route("/<int:user_id>/<int:sched_id>/")
def get_schedule(user_id, sched_id):
    """Get full details of a specific schedule."""
    schedule = GeneratedSchedule.query.filter_by(id=sched_id, user_id=user_id).first()
    if schedule is None:
        return failure_response("Schedule not found")

    return success_response(schedule.serialize())


@schedules_bp.route("/<int:user_id>/<int:sched_id>/", methods=["DELETE"])
def delete_schedule(user_id, sched_id):
    """Delete a saved schedule."""
    schedule = GeneratedSchedule.query.filter_by(id=sched_id, user_id=user_id).first()
    if schedule is None:
        return failure_response("Schedule not found")

    db.session.delete(schedule)
    db.session.commit()
    return success_response(schedule.serialize())


@schedules_bp.route("/generate/", methods=["POST"])
def generate_schedule():
    """Generate optimal schedules for a user using LLM + logic."""
    body = json.loads(request.data)
    user_id = body.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        return failure_response("User not found", code=404)

    completed = {c.course_number for c in user.completed_courses}
    availability = user.availability
    core_courses = {c.course_number for c in CoreClass.query.all()}
    num_core_completed = len(core_courses & completed)

    def is_grad_level(course_number):
        match = re.match(r"CS (\d{4})", course_number)
        return int(match.group(1)) >= 5000 if match else False

    def is_section_available(section, availability):
        day_index = {"M": 0, "T": 1, "W": 2, "R": 3, "F": 4}
        for d in section.days:
            if d not in day_index:
                continue
            day = day_index[d]
            for m in range(section.start_min, section.end_min, 60):
                hour = m // 60
                index = day + 7 * hour
                if index >= len(availability) or availability[index] == "0":
                    return False
        return True

    def has_prereqs(course, completed):
        number = course.number
        prereq_rules = {
            "CS 2110": [["CS 1110", "CS 1112"]],
            "CS 2112": [["CS 1110", "CS 1112"]],
            "CS 3110": [["CS 2110"], ["CS 2800", "CS 2802"]],
            "CS 3700": [["CS 2110"], ["CS 2800", "CS 2802"]],
            "CS 4410": [["CS 3410", "CS 3420"]],
            "CS 4414": [["CS 3410", "CS 3420"]],
        }

        if number in prereq_rules:
            return all(
                any(pr in completed for pr in group) for group in prereq_rules[number]
            )

        prereqs = [
            p.prereq_number
            for p in CoursePrereq.query.filter_by(course_number=number).all()
        ]
        return all(pr in completed for pr in prereqs)

    def sections_overlap(s1, s2):
        shared_days = set(s1.days) & set(s2.days)
        if not shared_days:
            return False
        return not (s1.end_min <= s2.start_min or s1.start_min >= s2.end_min)

    core_sections, elective_sections, grad_sections = [], [], []

    for course in Course.query.all():
        if course.number in completed:
            continue
        if not has_prereqs(course, completed):
            continue
        for section in course.sections:
            if not is_section_available(section, availability):
                continue
            pair = (course, section)
            if is_grad_level(course.number):
                grad_sections.append(pair)
            elif course.number in core_courses:
                core_sections.append(pair)
            else:
                elective_sections.append(pair)

    if not (core_sections or elective_sections or grad_sections):
        return failure_response("No available course sections match your schedule.")

    final_sections = []
    added_courses = set()

    # 1. Fill with core classes (up to 3)
    max_core = min(3 - num_core_completed, len(core_sections))
    for course, section in core_sections:
        if course.number not in added_courses and all(
            not sections_overlap(section, existing) for existing in final_sections
        ):
            final_sections.append(section)
            added_courses.add(course.number)
        if len(final_sections) >= max_core:
            break

    # 2. Fill remaining slots prioritizing interests
    remaining_slots = 5 - len(final_sections)
    if remaining_slots > 0 and elective_sections:
        ranked_electives = gpt_rank_courses(
            elective_sections, user.interests, remaining_slots
        )
        for course, section in ranked_electives:
            if (
                course.number not in added_courses
                and len(final_sections) < 5
                and all(
                    not sections_overlap(section, existing)
                    for existing in final_sections
                )
            ):
                final_sections.append(section)
                added_courses.add(course.number)

    # 3. Only consider grad classes if they've completed 3+ core classes
    remaining_slots = 5 - len(final_sections)
    if remaining_slots > 0 and num_core_completed >= 3 and grad_sections:
        for course, section in grad_sections:
            if (
                course.number not in added_courses
                and len(final_sections) < 5
                and all(
                    not sections_overlap(section, existing)
                    for existing in final_sections
                )
            ):
                final_sections.append(section)
                added_courses.add(course.number)

    # Create the schedule
    new_schedule = GeneratedSchedule(
        user_id=user_id,
        # score=1.0,
        rationale="Prioritized core classes, then ranked electives, then grad-level if eligible.",
    )
    db.session.add(new_schedule)
    db.session.commit()

    for sec in final_sections:
        db.session.add(ScheduleSection(schedule_id=new_schedule.id, section_id=sec.id))

    db.session.commit()
    return success_response(new_schedule.serialize(), 201)
