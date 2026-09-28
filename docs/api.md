# REST API Documentation

The **Smart Student Complaint Analyzer** exposes REST-style API endpoints for integrations, mobile clients, and external grievance portals.

---

## 1. NLP Real-Time Inference

### `POST /api/analyze`
Executes real-time natural language processing without modifying the database.

#### Request Headers:
`Content-Type: application/json`

#### Request Body:
```json
{
  "text": "The Wi-Fi in the central library is down and not working for 2 days."
}
```

#### Response: `200 OK`
```json
{
  "category": "IT & Wi-Fi",
  "confidence": 93.4,
  "department": "IT Support",
  "keywords": [
    "Wifi",
    "Library",
    "Work",
    "Central",
    "Day"
  ],
  "priority": "High",
  "sentiment": "Negative",
  "sentiment_score": -0.42
}
```

---

## 2. Complaint Management Endpoints

### `GET /api/complaints`
Retrieve a list of complaints.
- If authenticated as a **Student**, returns all grievances submitted by that student.
- If authenticated as an **Admin**, returns all institutional grievances.

#### Response: `200 OK`
```json
{
  "count": 1,
  "complaints": [
    {
      "id": 1,
      "student_id": 2,
      "student_name": "Aarav Sharma",
      "student_email": "student@smartcampus.com",
      "title": "Wi-Fi in Central Library is constantly disconnecting",
      "description": "The campus Wi-Fi router on the second floor has not been functioning...",
      "category": "IT & Wi-Fi",
      "sentiment": "Negative",
      "sentiment_score": -0.48,
      "priority": "High",
      "department": "IT Support",
      "confidence": 94.2,
      "keywords": ["Wifi", "Library", "Router", "Disconnect"],
      "status": "Resolved",
      "admin_response": "IT Support replaced the access point.",
      "created_at": "2026-09-10 14:30:00",
      "updated_at": "2026-09-11 09:15:00"
    }
  ]
}
```

---

### `POST /api/complaints`
Submit a new student grievance. The system will automatically execute NLP analysis on the text and persist the record.

#### Request Body:
```json
{
  "title": "Water cooler in block B is broken",
  "description": "There is no drinking water on the second floor for the past 24 hours."
}
```

#### Response: `201 Created`
```json
{
  "message": "Complaint submitted successfully",
  "complaint": {
    "id": 23,
    "title": "Water cooler in block B is broken",
    "category": "Infrastructure",
    "priority": "High",
    "status": "Pending",
    "confidence": 91.8
  }
}
```

---

### `PUT /api/complaints/<id>`
Update complaint status, assigned department, or post an official admin response (Admin only).

#### Request Body:
```json
{
  "status": "In Progress",
  "department": "Maintenance Department",
  "admin_response": "Maintenance technician dispatched to replace water filter valve."
}
```

#### Response: `200 OK`
```json
{
  "message": "Complaint updated successfully",
  "complaint": { ... }
}
```

---

### `DELETE /api/complaints/<id>`
Delete a complaint record (Admin only).

#### Response: `200 OK`
```json
{
  "message": "Complaint #23 deleted successfully"
}
```
