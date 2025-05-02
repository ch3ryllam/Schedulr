import json
from flask import Blueprint, request
from app.models import db, User, CompletedCourse
from ..utils import success_response, failure_response

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["POST"])
def create_user():
    """
    Create a new user profile.
    Takes in netid, graduation_year, interests, and availability.
    """
    body = json.loads(request.data)
    netid, grad_year = body.get("netid"), body.get("graduation_year")
    interests = body.get("interests")
    availability = body.get("availability")

    if None in (netid, grad_year, availability):
        return failure_response("Missing required fields", code=400)

    new_user = User(
        netid=netid,
        graduation_year=grad_year,
        interests=interests,
        availability=availability,
    )
    db.session.add(new_user)
    db.session.commit()

    return success_response(new_user.serialize(), code=201)


@users_bp.route("/")
def all_users():
    """
    Return a list of all users.
    """

    users = [user.serialize() for user in User.query.all()]
    return success_response({"users": users})


@users_bp.route("/<int:user_id>/")
def get_user(user_id):
    """Get user profile by ID."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")
    return success_response(user.serialize())


@users_bp.route("/<int:user_id>/", methods=["PATCH"])
def update_user(user_id):
    """
    Update user's profile.
    Data can include any of the fields but not none of them.
    Primarily used to update/add interests and availability
    """
    user = User.query.get(user_id)
    if user is None:
        return failure_response("User not found")

    body = json.loads(request.data)
    netid, grad_year, interests, availability = (
        body.get("netid"),
        body.get("graduation_year"),
        body.get("interests"),
        body.get("availability"),
    )
    attribute_list = [netid, grad_year, interests, availability]
    if all(x is None for x in attribute_list):
        return failure_response("Must provide a valid field to update", code=400)

    if netid is not None:
        user.netid = netid
    if grad_year is not None:
        user.graduation_year = grad_year
    if interests is not None:
        user.interests = interests
    if availability is not None:
        user.availability = availability

    db.session.commit()
    return success_response(user.serialize())


@users_bp.route("/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user and all their data.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")

    db.session.delete(user)
    db.session.commit()

    return success_response(user.serialize())


@users_bp.route("/<int:user_id>/completions/", methods=["GET"])
def list_completions(user_id):
    """
    Return all completed courses for this user.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")
    completions = user.serialize()["completed_courses"]

    return success_response({"completed_courses": completions})


@users_bp.route("/<int:user_id>/completions/", methods=["POST"])
def add_completion(user_id):
    """
    Mark a course as completed by the user.
    The body of the request should have a "course_number" field with the number of the course (eg. "CS 4820").
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")

    body = json.loads(request.data)
    course_number = body.get("course_number")
    if course_number is None:
        return failure_response("Must provide a course_number field.", code=400)

    if course_number[:3] != "CS ":
        return failure_response(
            "Course number must start with 'CS ' followed by the number.", code=400
        )
    completion = CompletedCourse(user_id=user_id, course_number=str(course_number))
    db.session.add(completion)
    db.session.commit()
    return success_response(completion.serialize(), code=201)


@users_bp.route("/<int:user_id>/completions/<int:course_number>", methods=["DELETE"])
def remove_completion(user_id, course_number):
    """
    Remove a completed course from this user.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")

    course_number = "CS " + str(course_number)
    completion = CompletedCourse.query.filter_by(
        user_id=user_id, course_number=course_number
    ).first()
    if completion is None:
        return failure_response("User has not completed that course.")

    db.session.delete(completion)
    db.session.commit()

    return success_response(completion.serialize())


@users_bp.route("/<int:user_id>/availability/", methods=["PATCH"])
def set_availability(user_id):
    """
    Set or update the user's availability bitmask.
    """

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")

    body = json.loads(request.data)
    availability = body.get("availability")
    if availability is None:
        return failure_response("Did not provide availability.", code=400)

    user.availability = availability
    db.session.commit()

    return success_response(user.serialize(), code=201)


@users_bp.route("/<int:user_id>/availability/", methods=["GET"])
def get_availability(user_id):
    """
    Return the user's current availability bitmask.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")

    return success_response({"availability": user.availability})
