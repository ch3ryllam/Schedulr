import json
from db import db, seed_courses, seed_core, seed_prereq, seed_schedules
from flask import Flask, request
from db import (
    db,
    CompletedCourse,
    CoursePrereq,
    CoreClass,
    User,
    Course,
    CourseSection,
    GeneratedSchedule,
    ScheduleSection,
)

def create_app():
    
    app = Flask(__name__)
    db_filename = "course.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_courses(app)
        seed_core(app)
        seed_prereq(app)
        seed_schedules(app)

    return app

app = create_app()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/users/", methods=["POST"])
def create_user():
    """
    Create a new user profile.
    Takes in netid and graduation_year.
    """
    body = json.loads(request.data)
    netid, grad_year = body.get("netid"), body.get("graduation_year")

    if None in (netid, grad_year):
        return failure_response("Missing netid or graduation_year", code=400)

    new_user = User(netid = netid, graduation_year = grad_year)
    db.session.add(new_user)
    db.session.commit()

    return success_response(new_user.serialize(), code=201)

@app.route("/users/")
def all_users():
    """
    Return a list of all users.
    """

    users = [user.serialize() for user in User.query.all()]
    return success_response({"users": users})


@app.route("/users/<int:user_id>/")
def get_user(user_id):
    """Get user profile by ID."""
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response("User not found.")
    return success_response(user.serialize())

@app.route("/users/<int:user_id>/", methods=["PATCH"])
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
    netid, grad_year, interests, availability =  body.get("netid"), body.get("graduation_year"), body.get("interests"), body.get("availability")
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

@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user and all their data.
    """
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response("User not found.")
    
    db.session.delete(user)
    db.session.commit()

    return success_response(user.serialize())

@app.route("/users/<int:user_id>/completions/")
def list_completions(user_id):
    """
    Return all completed courses for this user.
    """
    user = User.query.filter_by(id= user_id).first()
    if user is None:
        return failure_response("User not found.")
    completions = user.serialize()["completed_courses"]

    return success_response({"completed_courses": completions})

@app.route("/users/<int:user_id>/completions/", methods=["POST"])
def add_completion(user_id):
    """
    Mark a course as completed by the user.
    The body of the request should have a "course_number" field with the number of the course (eg. "CS 4820").
    """
    user = User.query.filter_by(id= user_id).first()
    if user is None:
        return failure_response("User not found.")
    
    body = json.loads(request.data)
    course_number = body.get("course_number")
    if course_number is None:
        return failure_response("Must provide a course_number field.", code= 400)
    
    if course_number[:3] != "CS ":
        return failure_response("Course number must start with 'CS ' followed by the number.", code= 400)
    completion = CompletedCourse(user_id= user_id, course_number= str(course_number))
    db.session.add(completion)
    db.session.commit()
    return success_response(completion.serialize(), code= 201)

@app.route("/users/<int:user_id>/completions/<int:course_number>", methods=["DELETE"])
def remove_completion(user_id, course_number):
    """
    Remove a completed course from this user.
    """
    user = User.query.filter_by(id= user_id).first()
    if user is None:
        return failure_response("User not found.")
    
    course_number = "CS "+ str(course_number)
    completion = CompletedCourse.query.filter_by(user_id= user_id, course_number= course_number). first()
    if completion is None:
        return failure_response("User has not completed that course.")
    
    db.session.delete(completion)
    db.session.commit()

    return success_response(completion.serialize())


@app.route("/users/<int:user_id>/availability/", methods=["PATCH"])
def set_availability(user_id):
    """
    Set or update the user's availability bitmask.
    """

    user = User.query.filter_by(id= user_id).first()
    if user is None:
        return failure_response("User not found.")
    
    body = json.loads(request.data)
    availability = body.get("availability")
    if availability is None:
        return failure_response("Did not provide availability.", code= 400)
    
    user.availability = availability
    db.session.commit()

    return success_response(user.serialize(), code= 201)

@app.route("/users/<int:user_id>/availability/")
def get_availability(user_id):
    """
    Return the user's current availability bitmask.
    """
    user = User.query.filter_by(id= user_id).first()
    if user is None:
        return failure_response("User not found.")
    
    return success_response({"availability": user.availability})

# Course routes

@app.route("/courses/")
def list_courses():
    """Return all CS courses in the catalog."""
    pass

@app.route("/courses/<int:number>/")
def get_course(number):
    """Get info about a single course."""
    pass

@app.route("/sections/")
def list_sections():
    """Return all CS course sections (Fall 2025)."""
    pass

@app.route("/core-sets/")
def get_core_courses():
    """Return the 7 core CS courses."""
    core_courses = [course.serialize() for course in CoreClass.query.all()]
    return success_response({"courses": core_courses})

# Schedule routes

@app.route("/schedules/<int:user_id>/")
def list_schedules(user_id):
    """List all generated schedules for a user."""
    pass

@app.route("/schedules/<int:user_id>/<int:sched_id>/")
def get_schedule(user_id, sched_id):
    """Get full details of a specific schedule."""
    pass

@app.route("/schedules/<int:user_id>/<int:sched_id>/", methods=["DELETE"])
def delete_schedule(user_id, sched_id):
    """Delete a saved schedule."""
    pass

@app.route("/schedule/generate/", methods=["POST"])
def generate_schedule():
    """Generate optimal schedules for a user using LLM + logic."""
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
