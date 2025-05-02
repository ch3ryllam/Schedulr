import requests
import re
from datetime import datetime
from app.models import db, Course, CoursePrereq, CourseSection, CoreClass

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

API_URL = (
    "https://classes.cornell.edu/api/2.0/search/classes.json?roster=FA24&subject=CS"
)


def time_to_min(time):
    """
    Helper function to convert to minutes since 00:00.
    """
    t = (time or "").strip()
    if not t:
        return None
    try:
        # uppercase AM/PM so strptime is happy
        dt = datetime.strptime(t.upper(), "%I:%M%p")
        return dt.hour * 60 + dt.minute
    except ValueError:
        # malformed time string—skip it
        return None


def extract_prereqs(text):
    """
    Finds any pattern of 2-5 uppercase letters + optional space/dash + 4 digits,
    eg. "CS 1110", "MATH 1920"
    """
    pattern = r"\b([A-Z]{2,5})[ -]?(\d{4})\b"
    matches = re.findall(pattern, text)
    return [f"{dept} {num}" for dept, num in matches]


def get_data_ready():
    """
    Prepares the data for man handling.
    """
    raw_data = requests.get(API_URL)
    raw_data.raise_for_status()
    data = raw_data.json()["data"]["classes"]

    return data


data = get_data_ready()


def seed_courses():
    """
    Adds all courses to the database.
    """
    if Course.query.first():
        return
    for clss in data:
        num = f"CS {clss['catalogNbr']}"
        name = clss.get("titleLong", "").strip()
        description = clss.get("description", "").strip()
        credits = int(float(clss["enrollGroups"][0].get("unitsMinimum", 0)))

        course = db.session.get(Course, num)
        if not course:
            course = Course(
                number=num, name=name, description=description, credits=credits
            )
            db.session.add(course)

    db.session.commit()


def seed_prereq():
    """
    Adds prereqs to the database.
    """
    if CoursePrereq.query.first():
        return
    for clss in data:
        num = f"CS {clss['catalogNbr']}"
        prereq_text = clss.get("catalogPrereqCoreq", "")

        for prereq in extract_prereqs(prereq_text):
            exists = (
                db.session.query(CoursePrereq)
                .filter_by(course_number=num, prereq_number=prereq)
                .first()
            )
            if not exists:
                real_prereq = CoursePrereq(course_number=num, prereq_number=prereq)
                db.session.add(real_prereq)
    db.session.commit()


def seed_schedules():
    """
    Adds the sections into the database.
    """
    if CourseSection.query.first():
        return

    for clss in data:
        catalog = clss["catalogNbr"]
        num = f"CS {catalog}"
        group = clss.get("enrollGroups", [])
        for sec in group[0].get("classSections", []):
            label = sec.get("ssrComponent", "").strip()
            section_number = sec.get("section", "").strip()
            section_label = label + " " + section_number
            for mt in sec.get("meetings", []):
                days = mt.get("pattern", "")
                raw_start = mt.get("timeStart", "")
                raw_end = mt.get("timeEnd", "")

                start = time_to_min(raw_start)
                end = time_to_min(raw_end)

                if start is None or end is None:
                    print(
                        f"Skipping {num} - {section_label}: start={raw_start}, end={raw_end}"
                    )
                    continue

                course_section = CourseSection(
                    course_number=num,
                    section=section_label,
                    days=days or "TBA",
                    start_min=start,
                    end_min=end,
                )
                db.session.add(course_section)
    db.session.commit()


# Not a scraper but its nicer here
def seed_core():
    """
    Adds all core courses into the database.
    """
    if CoreClass.query.first():
        return
    core_courses = [
        CoreClass(course_number="CS 1110"),
        CoreClass(course_number="CS 1112"),
        CoreClass(course_number="CS 2110"),
        CoreClass(course_number="CS 2800"),
        CoreClass(course_number="CS 3110"),
        CoreClass(course_number="CS 3410"),
        CoreClass(course_number="CS 3420"),
        CoreClass(course_number="CS 4410"),
        CoreClass(course_number="CS 4414"),
        CoreClass(course_number="CS 4820"),
    ]
    for course in core_courses:
        if not CoreClass.query.filter_by(course_number=course.course_number).first():
            db.session.add(course)

    db.session.commit()
