# Schedulr

## Table of Contents
- [Application Description](#application-description)
- [Implemented Features](#implemented-features)
- [Database Models](#database-models)
- [GPT Integration](#gpt-integration)
- [Third-Party Tools & APIs](#third-party-tools--apis)
- [API Endpoint Reference](#api-endpoint-reference)

## Application Description

This backend powers the **Schedulr**, a scheduling assistant for Cornell CS students. It includes user profile management, course catalog access, prerequisite tracking, and schedule generation via GPT.

### Implemented Features

#### Routes
- `POST /users/`: Create a user with netid, grad year, interests, and availability.
- `GET /users/`: Get all users.
- `GET /users/<user_id>/`: Get user details.
- `PATCH /users/<user_id>/`: Update user fields.
- `DELETE /users/<user_id>/`: Delete user and all associated data.
- `GET /users/<user_id>/completions/`: List completed CS courses.
- `POST /users/<user_id>/completions/`: Add a completed course.
- `DELETE /users/<user_id>/completions/<course_number>/`: Remove a completed course.
- `GET /users/<user_id>/availability/`: Get availability bitmask.
- `PATCH /users/<user_id>/availability/`: Update availability.

- `GET /courses/`: Get all CS courses (with number, name, credits, description).
- `GET /courses/<number>/`: Get a course's sections, prerequisites, and dependents.

- `GET /sections/`: List all sections.
- `GET /sections/<section_id>/`: Get section details.

- `GET /core-sets/`: List required core CS courses.

- `POST /schedules/generate/`: Generate an optimal schedule (max 5 courses).
- `GET /schedules/<user_id>/`: List user’s schedules.
- `GET /schedules/<user_id>/<sched_id>/`: Get schedule details.
- `DELETE /schedules/<user_id>/<sched_id>/`: Delete a schedule.

### Database Models
- **User**: `netid`, `graduation_year`, `interests`, `availability`
- **Course**: `number`, `name`, `description`, `credits`, `sections`
- **CourseSection**: Linked to a course. Has days, times, and section code.
- **CoreClass**: 7 CS core courses.
- **CompletedCourse**: Link table recording which courses each user has completed.
- **CoursePrereq**: Records course-to-course prerequisites.
- **GeneratedSchedule**: A proposed set of course sections for a user.
- **ScheduleSection**: Link table mapping sections to a generated schedule.

### GPT Integration
- Used in `POST /schedules/generate/` to rank electives by user interests.
- GPT prompt includes:
  - Interests
  - Prerequisite assumptions
  - CS course equivalency rules (e.g. CS 2110 vs CS 2112)
  - Scheduling constraints (e.g. no CS 3110 with CS 3410)

### Third-Party Tools
- **OpenAI API** – Used to  rank elective courses based on user interests during schedule generation via GPT-4
- **Cornell Class Roster API** - Used to scrape live CS course offerings, prerequisites, and section times for Fall 2024.
- **Flask** – Python web framework for building the backend API
- **SQLAlchemy** – ORM for managing relational data models and database interactions.



## API Endpoint Refrence

## Users

### Create a User
**POST** `/users/`

**Request Body**
```json
{
  "netid": "rm834",
  "graduation_year": 2026,
  "interests": "AI, systems, HCI",
  "availability": "111111111111111111111111111111111111111111111111111111111111" // binary string of 168 chars (7 days * 24 hours)
}
```

**Response**
```json
<HTTP STATUS 201>
{
  "id": 1,
  "netid": "rm834",
  "graduation_year": 2026,
  "interests": "AI, systems, HCI",
  "availability": "111111111111111111111111111111111111111111111111111111111111"
}
```

---

### Get All Users
**GET** `/users/`

**Response**
```json
<HTTP STATUS 200>
{
  "users": [ { ... }, ... ]
}
```

---

### Get a Specific User
**GET** `/users/<user_id>/`

**Response**
```json
<HTTP STATUS 200>
{
  "id": 1,
  "netid": "rm834",
  "graduation_year": 2026,
  "interests": "AI, systems",
  "availability": "..."
}
```

---

### Update a User
**PATCH** `/users/<user_id>/`

**Request Body**
Fields are optional (must include at least one):
```json
{
  "interests": "updated",
  "availability": "000011110000..."
}
```

**Response**
```json
<HTTP STATUS 200>
{ ...updated user... }
```

---

### Delete a User
**DELETE** `/users/<user_id>/`

**Response**
```json
<HTTP STATUS 200>
{
  "id": <int>,
  "netid": <string>,
  "graduation_year": <string>,
  "interests": <string>,
  "availability": <string>,
  "completed_courses": [
    { "course_number": <string> },
    ...
  ],
  "generated_schedules": [
    {
      "id": <int>,
      "user_id": <int>,
      "rationale": <string or null>,
      "score": <float>
    },
    ...
  ]
}

```

---

## Courses

### Get All Courses
**GET** `/courses/`

**Response**
```json
<HTTP STATUS 200>
{
  "courses": [ { "number": "CS 1110", "name": "Intro to CS", ... }, ... ]
}
```

---

### Get a Specific Course
**GET** `/courses/<int:number>/`

**Response**
```json
<HTTP STATUS 200>
{
  "number": "CS 2110",
  "name": "Object-Oriented Programming and Data Structures",
  "description": "<string>",
  "credits": <int>,
  "sections": [
    {
      "id": <int>,
      "section": "<string>",
      "days": "<string>",
      "start_min": <int>,
      "end_min": <int>
    },
    ...
  ],
  "prereqs": [
    { "prereq_number": "<CS course number>" },
    ...
  ],
  "required_by": [
    { "course_number": "<CS course number>" },
    ...
  ]
}
```

---

## Completed Courses

### List Completed Courses
**GET** `/users/<user_id>/completions/`

**Response**
```json
<HTTP STATUS 200>
{
  "completed_courses": [ "CS 1110", "CS 2110" ]
}
```

---

### Add a Completed Course
**POST** `/users/<user_id>/completions/`

**Request Body**
```json
{ "course_number": "CS 2800" }
```

**Response**
```json
<HTTP STATUS 201>
{ "course_number": "CS 2800", "user_id": 1 }
```

---

### Remove a Completed Course
**DELETE** `/users/<user_id>/completions/<course_number>/`

**Response**
```json
<HTTP STATUS 200>
{ ...deleted completion... }
```

---

## Availability

### Get Availability
**GET** `/users/<user_id>/availability/`

### Update Availability
**PATCH** `/users/<user_id>/availability/`

**Request Body**
```json
{ "availability": "0110011..." }
```

---

## Core Courses

**GET** `/core-sets/`

**Response**
```json
{ "courses": [ "CS 1110", "CS 2110", ... ] }
```

---

## Schedule

### Generate a Schedule
**POST** `/schedules/generate/`

**Request Body**
```json
{ "user_id": 1 }
```

**Response**
```json
<HTTP STATUS 201>
{
  "id": 1,
  "user_id": 1,
  "score": 1.0,
  "rationale": "...",
  "sections": [
    { "course_number": "CS 2110", "section": "LEC 001", "days": "MWF", ... },
    ...
  ]
}
```

---

### List All Schedules for User
**GET** `/schedules/<user_id>/`

### Get Specific Schedule
**GET** `/schedules/<user_id>/<sched_id>/`

### Delete Schedule
**DELETE** `/schedules/<user_id>/<sched_id>/`