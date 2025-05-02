import re
from openai import OpenAI

client = OpenAI()


def gpt_rank_courses(courses, interests, remaining_slots):
    if not interests or len(courses) <= 1:
        return courses[:remaining_slots]
    try:
        prompt = f"""
            You are a course advisor helping a CS undergraduate student plan their next semester.
            The student is interested in: {interests}
            Rules & Assumptions:
            - The student has completed all non-CS prerequisites (e.g., Math or Engineering requirements).
            - The student may only take **one of each course pair**: CS 1110 or CS 1112, CS 2110 or CS 2112, CS 2800 or CS 2802, CS 3410 or CS 3420, CS 3700 or CS 3780, CS 4410 or CS 4414.
            - If both are available, choose the **non-honors/default version** (e.g., prefer CS 2110 over 2112, CS 2800 over 2802).
            - CS 3110 should not be taken concurrently with CS 3410 or 3420.
            - CS 3110 requires CS 2110 and CS 2800 (2800 can be a corequisite).
            - CS 3700 requires CS 2110 and CS 2800 as prerequisites.
            - CS 4410 requires CS 3410 or CS 3420.
            - Rank only the unique courses (avoid suggesting multiple sections of the same course).
            Courses to rank:
            {', '.join([course.number + ' - ' + course.name for course, _ in courses])}
            Respond with a comma-separated list of course numbers only in ranked order.
            """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Changed to more reliable model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful academic advisor.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        ranked_numbers = response.choices[0].message.content.split(",")
        ranked_numbers = [c.strip() for c in ranked_numbers if c.strip()]

        ranked = []
        for num in ranked_numbers:
            for pair in courses:
                if pair[0].number == num and pair not in ranked:
                    ranked.append(pair)

        for pair in courses:
            if pair not in ranked:
                ranked.append(pair)

        return ranked[:remaining_slots]

    except Exception as e:
        print(f"GPT Error: {e}")
        return courses[:remaining_slots]
