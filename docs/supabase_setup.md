# Supabase PostgreSQL Integration Guide

This guide explains how to connect your **Smart Student Complaint Analyzer** to a free cloud-hosted **Supabase PostgreSQL** database.

---

## 1. Create Your Free Supabase Database
1. Go to [https://supabase.com](https://supabase.com) and Sign In / Sign Up.
2. Click **New Project**.
3. Fill in:
   - **Project Name**: `student-complaint-analyzer`
   - **Database Password**: Choose a strong password (remember this password!).
   - **Region**: Choose the region closest to you.
4. Click **Create new project** and wait ~1-2 minutes for provisioning.

---

## 2. Execute the Database Schema in Supabase
1. In your Supabase project dashboard, click on the **SQL Editor** tab (terminal icon on left sidebar).
2. Click **+ New Query**.
3. Open [`supabase_schema.sql`](file:///f:/CodeStuff/StudentComplaintAnalyzer/supabase_schema.sql) in this project, copy its entire contents, and paste it into the Supabase SQL editor.
4. Click **Run** (green button).
5. You should see: `Success. No rows returned`.
6. To verify, click on the **Table Editor** icon on the left menu. You will see the `users` table and `complaints` table populated with sample records!

---

## 3. Retrieve Your Supabase Database Connection URI
1. In your Supabase project dashboard, click **Project Settings** (gear icon at bottom left).
2. Click on **Database** under Configuration.
3. Scroll down to the **Connection parameters** / **Connection string** section.
4. Select the **URI** tab.
5. You can choose either:
   - **Direct Connection** (Port 5432):
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres?sslmode=require
     ```
   - **Session / Transaction Pooler** (Port 6543 / 5432, recommended for all networks):
     ```
     postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require
     ```
6. Replace `[YOUR-PASSWORD]` with your actual database password.

---

## 4. Configure Your Flask Application
1. In your project root (`f:\CodeStuff\StudentComplaintAnalyzer`), create or edit `.env`.
2. Add your Supabase URI:

```env
SECRET_KEY=smartcampus-super-secret-key-2026
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres?sslmode=require
```

---

## 5. Run the Application
```powershell
# Activate your virtual environment
.\venv\Scripts\Activate.ps1

# Run the Flask app
python app.py
```

The application will now read and write directly to your live **Supabase PostgreSQL database**!
