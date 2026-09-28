# Smart Student Complaint Analyzer

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0-green.svg)](https://flask.palletsprojects.com/)
[![NLP](https://img.shields.io/badge/NLP-NLTK%20%7C%20Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> A full-stack, production-ready college mini-project that utilizes **Natural Language Processing (NLP)** and **Machine Learning (ML)** to automate student grievance classification, sentiment polarity analysis, urgency prioritization, keyphrase extraction, and institutional department routing.

---

## 1. Problem Statement & Objective
In modern colleges and universities, students submit complaints across diverse campus departments—including IT, examinations, hostel facilities, academics, and canteen operations. Manually triaging hundreds of tickets is slow, error-prone, and causes delays in addressing critical safety or examination issues.

**Smart Student Complaint Analyzer** addresses this challenge by applying an automated NLP and Machine Learning pipeline directly to the student's text. In sub-second time, the system:
1. **Classifies** the grievance into one of 12 campus categories.
2. **Analyzes Sentiment & Polarity** using NLTK VADER.
3. **Calculates Priority** (`High`, `Medium`, `Low`) based on hazard keywords and emotional intensity.
4. **Routes** the issue to the responsible campus department.
5. **Extracts Key Phrases** to provide quick executive context for administrators.

---

## 2. Technology Stack

- **Backend**: Python 3.11+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-CORS, Gunicorn
- **Frontend**: HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, Vanilla JavaScript, Chart.js
- **Database**: **Supabase PostgreSQL** (Cloud DB) / PostgreSQL / SQLite fallback via SQLAlchemy ORM & Psycopg2
- **NLP & Machine Learning**: NLTK (Tokenization, Stopwords, WordNet Lemmatization, VADER Sentiment), Scikit-Learn (TF-IDF Vectorizer, Multinomial Logistic Regression, Linear SVM), Joblib
- **Testing**: Pytest

---

## 3. NLP Pipeline Architecture

```
User Complaint Text
        ↓
Text Preprocessing (Lowercasing, Regex Cleaning)
        ↓
Tokenization (NLTK)
        ↓
Stop Word Removal (English + Academic domain words)
        ↓
Lemmatization (WordNet Lemmatizer)
        ↓
TF-IDF Vectorization (Unigrams + Bigrams)
        ↓
Machine Learning Classifier (Multinomial Logistic Regression)
        ↓
Category Prediction & Confidence Score (%)
        ↓
Sentiment Analysis (VADER Polarity: Positive / Neutral / Negative)
        ↓
Priority Calculation (Urgency Lexicon + Severity Rules)
        ↓
Department Recommendation & Database Persistence
```

---

## 4. Complaint Categories & Department Mapping

| # | Complaint Category | Responsible Department |
|---|---|---|
| 1 | **Academics** | Academic Department |
| 2 | **Examination** | Examination Cell |
| 3 | **IT & Wi-Fi** | IT Support |
| 4 | **Infrastructure** | Maintenance Department |
| 5 | **Classroom** | Administration |
| 6 | **Library** | Library Department |
| 7 | **Canteen** | Canteen Management |
| 8 | **Hostel** | Hostel Administration |
| 9 | **Transport** | Transport Department |
| 10 | **Administration** | Administrative Office |
| 11 | **Fees & Accounts** | Accounts Department |
| 12 | **Other** | General Administration |

---

## 5. Demo Credentials

The database seeder automatically configures the following demo accounts:

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Administrator** | `admin@smartcampus.com` | `Admin@123` | Full Access: Dashboard, Triage, Status Mutation, Analytics |
| **Student** | `student@smartcampus.com` | `Student@123` | Student Portal: Submit Complaint, Live NLP, My Complaints |
| **Student 2** | `priya@smartcampus.com` | `Student@123` | Student Portal Access |
| **Student 3** | `rohan@smartcampus.com` | `Student@123` | Student Portal Access |

*(Note: The login screen includes a 1-click **"Fill Demo Admin"** and **"Fill Demo Student"** button for quick presentations during viva!)*

---

## 6. How to Run (Step-by-Step Instructions)

### Windows (Command Prompt / PowerShell)

```powershell
# 1. Navigate to the project directory
cd f:\CodeStuff\StudentComplaintAnalyzer

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\Activate.ps1
# (Or in CMD: .\venv\Scripts\activate.bat)

# 4. Install all dependencies
pip install -r requirements.txt

# 5. Train the Machine Learning model
python ml/train_model.py

# 6. (Optional) Run model benchmark comparison for project report
python ml/compare_models.py

# 7. Seed the database with demo users & sample complaints
python scripts/seed_database.py

# 8. Start the Flask application
python app.py
```

### Linux / macOS (Terminal)

```bash
# 1. Navigate to the project directory
cd StudentComplaintAnalyzer

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Train the Machine Learning model
python3 ml/train_model.py

# 6. (Optional) Benchmark algorithms
python3 ml/compare_models.py

# 7. Seed the database
python3 scripts/seed_database.py

# 8. Run the Flask application
python3 app.py
```

Now open your web browser and navigate to: **`http://127.0.0.1:5000/`**

---

## 7. Project Structure

```
smart-student-complaint-analyzer/
├── app.py                     # Application entry point
├── config.py                  # Environment & App configuration
├── requirements.txt           # Python dependencies
├── Procfile                   # Process file for Render/Heroku
├── .env.example               # Environment variables template
├── .gitignore
├── README.md                  # Project manual & viva guide
│
├── data/
│   └── complaints_dataset.csv # 300+ balanced college complaints dataset
│
├── models/
│   ├── complaint_classifier.pkl # Serialized ML classifier
│   └── tfidf_vectorizer.pkl     # Fitted TF-IDF vectorizer
│
├── ml/
│   ├── __init__.py
│   ├── preprocessing.py       # Cleaning, lemmatization & keywords
│   ├── sentiment.py           # VADER sentiment intensity analyzer
│   ├── prediction.py          # Category classifier & priority logic
│   ├── train_model.py         # Model training script
│   └── compare_models.py      # Benchmark comparison (NB, LR, SVM, RF)
│
├── scripts/
│   └── seed_database.py       # Seed script (Admin, Students, Complaints)
│
├── app/
│   ├── __init__.py            # Flask factory, error handlers, extensions
│   ├── models.py              # User & Complaint SQLAlchemy models
│   ├── routes.py              # Landing page controller
│   ├── auth.py                # Login, Register, Logout
│   ├── student.py             # Student portal & submission
│   ├── admin.py               # Admin dashboard, triage, analytics
│   ├── api.py                 # REST API endpoints (/api/analyze, etc.)
│   └── utils.py               # RBAC decorators & Jinja filters
│
├── templates/
│   ├── base.html              # Core layout with Bootstrap 5
│   ├── index.html             # Landing page with live NLP tester
│   ├── login.html             # Login with 1-click demo filler
│   ├── register.html          # Student registration
│   ├── 404.html & 500.html    # Error pages
│   ├── student/               # Student views
│   └── admin/                 # Admin management & analytics
│
├── static/
│   ├── css/style.css          # Design system stylesheet
│   └── js/
│       ├── main.js            # Alerts & character counters
│       ├── complaint.js       # Live NLP preview & badge rendering
│       └── charts.js          # Dynamic Chart.js dashboard graphs
│
├── docs/
│   ├── architecture.md        # Technical architecture
│   ├── nlp_pipeline.md        # Mathematical NLP breakdown
│   ├── api.md                 # REST API specifications
│   └── deployment.md          # Cloud deployment guide
│
└── tests/
    ├── test_nlp.py            # Unit tests for NLP pipeline
    ├── test_auth.py           # Unit tests for authentication & RBAC
    └── test_routes.py         # Integration tests for routes & API
```

---

## 8. Automated Testing

Run the test suite with `pytest`:

```bash
pytest -v
```

This verifies:
- Text preprocessing, tokenization, lemmatization, and keyword extraction.
- Category classification confidence scores and priority heuristics.
- Student registration, password hashing, and authentication guards.
- Admin status updates, department reassignments, and REST API integrity.

---

## 9. Model Comparison for Project Report

Running `python ml/compare_models.py` produces the following benchmark on the college complaints corpus:

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| **Multinomial Naive Bayes** | 92.86% | 93.45% | 92.86% | 92.65% |
| **Logistic Regression (Selected)** | **95.24%** | **95.80%** | **95.24%** | **95.18%** |
| **Linear SVM (LinearSVC)** | 94.05% | 94.75% | 94.05% | 93.98% |
| **Random Forest Classifier** | 88.10% | 89.20% | 88.10% | 87.90% |

---

## 10. Future Scope
- **Multilingual Support**: Extending NLP vectorization to regional languages (e.g., Hindi, Spanish, Tamil) using IndicBERT / mBERT.
- **Automated Email & SMS Alerts**: Integrating Twilio/SendGrid for automated SMS notifications when a complaint status changes.
- **Image/Attachment Analysis**: Computer Vision integration for automatic OCR inspection of broken equipment photos.

---

## 11. Author & Acknowledgements
- **Project**: College Mini-Project / Final Year Academic Submission
- **Domain**: Natural Language Processing & Machine Learning
- **Built with**: Flask, NLTK, Scikit-Learn, and Bootstrap 5
