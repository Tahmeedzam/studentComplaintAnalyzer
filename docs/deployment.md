# Deployment Guide - Smart Student Complaint Analyzer

This guide details step-by-step instructions for deploying the **Smart Student Complaint Analyzer** to production cloud platforms like **Render**, **Railway**, or **Heroku**, using **Gunicorn** and **PostgreSQL**.

---

## 1. Prerequisites
- A GitHub repository with this codebase pushed.
- A free cloud hosting account (e.g., [Render.com](https://render.com)).
- Pre-trained model artifacts (`models/complaint_classifier.pkl` & `models/tfidf_vectorizer.pkl`) included or generated during build.

---

## 2. Deploying to Render (Recommended Free/Low-Cost Tier)

### Step 1: Create a PostgreSQL Database on Render
1. Log in to your Render Dashboard.
2. Click **New +** $\rightarrow$ **PostgreSQL**.
3. Name your database (e.g., `smartcampus-db`).
4. Select the Free tier and click **Create Database**.
5. Copy the **Internal Database URL** (or External URL).

### Step 2: Create a Web Service
1. Click **New +** $\rightarrow$ **Web Service**.
2. Connect your GitHub repository.
3. Configure the service settings:
   - **Name**: `student-complaint-analyzer`
   - **Environment**: `Python 3`
   - **Region**: Closest to your users
   - **Branch**: `main`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python ml/train_model.py && python scripts/seed_database.py
     ```
   - **Start Command**:
     ```bash
     gunicorn app:app
     ```

### Step 3: Set Environment Variables
Under the **Environment** tab, add the following key-value pairs:

| Key | Example Value | Description |
|---|---|---|
| `FLASK_ENV` | `production` | Enables production configurations |
| `SECRET_KEY` | `generate-a-strong-random-secret-key` | Session cryptographic encryption |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/dbname` | Render PostgreSQL connection string |
| `PYTHONUNBUFFERED` | `1` | Stream console logs in real time |

4. Click **Deploy Web Service**.
5. Once deployment completes, your application will be live at `https://your-service-name.onrender.com`.

---

## 3. Database Migration: SQLite to PostgreSQL
The application uses SQLAlchemy ORM which abstracts the underlying SQL dialect:
- For **Local Development**: `DATABASE_URL` defaults to `sqlite:///instance/database.db`.
- For **Production**: Set `DATABASE_URL` to your PostgreSQL URI (e.g., `postgresql://...`).
- When the application boots, `db.create_all()` automatically provisions all tables in PostgreSQL.
