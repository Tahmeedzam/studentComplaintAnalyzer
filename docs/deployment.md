# Deployment Guide - Smart Student Complaint Analyzer

This guide details step-by-step instructions for deploying the **Smart Student Complaint Analyzer** to **Vercel** (Quickest & Free) as well as **Render** using **Supabase PostgreSQL**.

---

## ⚡ Option 1: Deploy to Vercel (Quickest & Recommended)

Vercel provides the fastest, serverless hosting for Python Flask web applications.

### Prerequisites:
1. Your project is pushed to a **GitHub repository**.
2. A **Supabase PostgreSQL** database is set up (see [`docs/supabase_setup.md`](supabase_setup.md)).

### Step 1: Import Project in Vercel
1. Go to [https://vercel.com](https://vercel.com) and log in with your GitHub account.
2. Click **"Add New..."** $\rightarrow$ **"Project"**.
3. Select your `StudentComplaintAnalyzer` repository and click **"Import"**.

### Step 2: Configure Environment Variables
Before clicking deploy, expand the **"Environment Variables"** section and add:

| Key | Example Value | Description |
|---|---|---|
| `SECRET_KEY` | `smartcampus-super-secret-key-2026` | Flask session encryption key |
| `FLASK_ENV` | `production` | Enables production mode |
| `DATABASE_URL` | `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres?sslmode=require` | Your Supabase connection string |

### Step 3: Deploy
1. Click **"Deploy"**.
2. Vercel will automatically read `vercel.json`, install `requirements.txt`, and deploy the Flask serverless backend in under 60 seconds!
3. Your app is live at `https://your-project-name.vercel.app` 🎉.

---

## 🚀 Option 2: Deploy to Render

1. Log in to [https://render.com](https://render.com).
2. Click **"New +"** $\rightarrow$ **"Web Service"** and connect your GitHub repo.
3. Configure:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python ml/train_model.py`
   - **Start Command**: `gunicorn app:app`
4. Add Environment Variables:
   - `SECRET_KEY`: `smartcampus-super-secret-key-2026`
   - `DATABASE_URL`: `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres?sslmode=require`
5. Click **"Deploy Web Service"**.
