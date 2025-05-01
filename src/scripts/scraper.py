import requests
import re
from datetime import datetime
from db import db, Course, CoursePrereq, CourseSection, CoreClass

"""
Scraper that goes through the cornell CS catalogue using the cornell API 
and adds relevant details to their respective tables.
"""

# ------- WEB SCRAPER --------
# In terms of course:
# - Number (eg. "CS 1110")
# - Name (eg. "Introduction to computing")
# - Decription (eg. "This course focuses on...")
# - Credits (eg. 4)
# 
# In terms of CoursePrereq:
#  - Number
#  - Prereq number (multiple rows if more than 1 prereq)

# In terms of CourseSection:
#  - Number
#  - Section (eg. LEC 001, DIS 201)
#  - Days (eg. MWF)
#  - Start_time (in minutes since 00:00)
#  - End_time (in minutes since 00:00)

API_URL = "https://classes.cornell.edu/api/2.0/config/FA25/class.json?subject=CS"


def time_to_min(time):
    """
    Helper function to convert to minutes since 00:00.
    """
    dt = datetime.strptime(time.strip().lower(), "%I:%M%p")
    return dt.hour * 60 + dt.minute

def extract_prereqs(text):
    """
    Finds any pattern of 2-5 uppercase letters + optional space/dash + 4 digits,
    eg. "CS 1110", "MATH 1920"
    """
    pattern = r"\b([A-Z]{2,5})[ -]?(\d{4})\b"
    matches = re.findall(pattern, text)
    return [f"{dept} {num}" for dept, num in matches]

def seed_courses(app):
    pass

def seed_prereq(app):
    pass

def seed_schedules(app):
    pass


# Not a scraper but its nicer here
def seed_core(app):
    with app.app_context():
        core_courses = [CoreClass(course_number= "CS 1110"), CoreClass(course_number= "CS 1112"), CoreClass(course_number= "CS 2110"), 
                        CoreClass(course_number= "CS 2800"), CoreClass(course_number= "CS 3110"), CoreClass(course_number= "CS 3410"), 
                        CoreClass(course_number= "CS 3420"), CoreClass(course_number= "CS 4410"), CoreClass(course_number= "CS 4414"), 
                        CoreClass(course_number= "CS 4820")]
        for course in core_courses:
            if not CoreClass.query.filter_by(course_number= course.course_number).first():
                db.session.add(course) 
        
        db.session.commit()
        print("Seeded core courses")