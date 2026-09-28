# System Architecture - Smart Student Complaint Analyzer

## 1. Overview
The **Smart Student Complaint Analyzer** is an end-to-end full-stack web application designed for educational institutions to automate the triage, classification, prioritization, and tracking of student grievances using Natural Language Processing (NLP) and Machine Learning (ML).

---

## 2. Architecture Layers

```
+-------------------------------------------------------------+
|                  Presentation Layer                         |
|  - Bootstrap 5 + Vanilla JS + Chart.js                      |
|  - Responsive UI (Student Portal & Admin Command Center)    |
|  - Real-time NLP Live Playground & Interactive Previews     |
+-------------------------------------------------------------+
                              |
                              v (HTTP / REST API / Form Submissions)
+-------------------------------------------------------------+
|                  Application & Route Layer                  |
|  - Flask Application Factory                                |
|  - Blueprints: Auth, Student, Admin, API, Public Routes     |
|  - Session Authentication & RBAC (Flask-Login)              |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                  NLP & Machine Learning Engine              |
|  - Text Preprocessing (Cleaning, Lemmatization, Stopwords)  |
|  - Feature Vectorization (TF-IDF N-grams)                   |
|  - Category Classification (Multinomial Logistic Regression)|
|  - Sentiment Analysis (NLTK VADER Intensity Scoring)        |
|  - Priority Calculation Heuristic Engine                    |
|  - Keyphrase & Keyword Extraction                           |
+-------------------------------------------------------------+
                              |
                              v (SQLAlchemy ORM)
+-------------------------------------------------------------+
|                     Data Storage Layer                      |
|  - SQLite (Local Development)                               |
|  - PostgreSQL (Production / Cloud Deployment)               |
+-------------------------------------------------------------+
```

---

## 3. Database Schema

### Users Table (`users`)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique user identifier |
| `name` | String(120) | Not Null | User's full name |
| `email` | String(120) | Unique, Index, Not Null | Institutional email |
| `password_hash` | String(255) | Not Null | Scrypt / PBKDF2 hashed password |
| `role` | String(20) | Not Null, Default: 'student' | Access role (`student` or `admin`) |
| `created_at` | DateTime | Default: UTC Now | Account creation timestamp |

### Complaints Table (`complaints`)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Complaint tracking ID |
| `student_id` | Integer | ForeignKey(`users.id`), Index | Submitter reference |
| `title` | String(200) | Not Null | Grievance title |
| `description` | Text | Not Null | Detailed problem description |
| `category` | String(80) | Not Null | ML-predicted category (e.g. IT & Wi-Fi) |
| `sentiment` | String(30) | Not Null | Sentiment label (`Positive`, `Neutral`, `Negative`) |
| `sentiment_score` | Float | Default: 0.0 | VADER compound score ($-1.0$ to $+1.0$) |
| `priority` | String(20) | Not Null | Calculated urgency (`High`, `Medium`, `Low`) |
| `department` | String(100) | Not Null | Recommended department |
| `confidence` | Float | Default: 0.0 | Model classification probability (%) |
| `keywords` | Text | Default: `[]` | JSON serialized list of extracted terms |
| `status` | String(30) | Default: 'Pending' | `Pending`, `In Progress`, `Resolved`, `Rejected` |
| `admin_response` | Text | Nullable | Official administrative resolution note |
| `created_at` | DateTime | Index, Default: UTC Now | Submission timestamp |
| `updated_at` | DateTime | Default: UTC Now | Last status modification timestamp |

---

## 4. Security & Role-Based Access Control (RBAC)
- **Password Security**: Passwords are securely hashed using Werkzeug security utilities. Plain text passwords are never stored.
- **Session Protection**: Flask-Login protects session cookies with strict HTTPOnly and samesite policies.
- **Access Decorators**: Custom `@admin_required` and `@student_required` wrappers prevent privilege escalation.
- **Data Isolation**: Students can only view their own grievance history; administrators have full institutional visibility.
