
### Get All Courses
**GET /api/courses/**

Returns a list of all CS courses in the catalog.

#### Response
**Status Code**: 200 OK  
**Body**:
```json
{
  "courses": [
    {
      "number": "CS 1110",
      "name": "Intro to Computing Using Python",
      "description": "Introduction to programming and problem solving using Python.",
      "credits": 4,
      "prerequisites": [],
      "required_by": ["CS 2110", "CS 2800"]
    },
    {
      "number": "CS 2110",
      "name": "Object-Oriented Programming and Data Structures",
      "description": "Intermediate programming with a focus on data structures and object-oriented design.",
      "credits": 3,
      "prerequisites": ["CS 1110"],
      "required_by": ["CS 3110", "CS 3700"]
    }
  ]
}
```

- `number`: Course code (e.g., "CS 1110")
- `name`: Full course title
- `description`: Short course summary
- `credits`: Number of credit hours
- `prerequisites`: List of course numbers required before taking this course
- `required_by`: List of course numbers that list this course as a prerequisite


# Course Scheduling API Specification

## Base URL
```
http://localhost:5000
```

---

## Users

### Create a User
**POST** `/users/`

**Request Body**
```json
{
  "netid": "rm834",
  "graduation_year": 2026,
  "interests": "AI, systems, HCI",
  "availability": "111111111111111111111111111111111111111111111111111111111111"
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
{ ...deleted user data... }
```

---

## Courses

### Get All Courses
**GET** `/courses/`

**Response**
```json
<HTTP STATUS 200>
{
  "courses": [ { 
    "number": "CS 1110", 
    "name": "Intro to CS", 
    "description": "Introduction to programming and problem solving using Python.",
    "credits": 4,
    "prerequisites": [],
    "required_by": ["CS 2110", "CS 2800"] }, ... ]
}
```

---

### Get a Specific Course
**GET** `/courses/<int:number>/`

**Response**
```json
<HTTP STATUS 200>
{ "number": "CS 1110", "name": "Intro to CS", ... }
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
**POST** `/schedule/generate/`

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