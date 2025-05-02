# Course App API Specification

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