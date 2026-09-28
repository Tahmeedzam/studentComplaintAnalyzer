# 🚀 Quickstart Guide: Running Smart Student Complaint Analyzer on Any Device

Follow these instructions to clone and run this project on any Windows, macOS, or Linux machine.

---

## 🔑 1. Demo Login Credentials

Use these pre-configured credentials to test the application:

| Role | Email Address | Password | Permissions |
|---|---|---|---|
| **Administrator** | `admin@smartcampus.com` | `Admin@123` | Full Admin Dashboard, Triage, Status Updates, Analytics |
| **Student (Demo 1)** | `student@smartcampus.com` | `Student@123` | Submit Complaints, Live NLP Preview, Track Status |
| **Student (Demo 2)** | `priya@smartcampus.com` | `Student@123` | Student Portal Access |
| **Student (Demo 3)** | `rohan@smartcampus.com` | `Student@123` | Student Portal Access |

> 💡 **Viva Tip:** On the `/login` page, you can click the **"Fill Admin"** or **"Fill Student"** buttons to automatically fill the credentials in 1 click!

---

## 💻 2. Running on Windows

Open **PowerShell** or **Command Prompt** and run:

```powershell
# Step 1: Clone the repository (replace with your repo URL)
git clone https://github.com/YOUR_USERNAME/StudentComplaintAnalyzer.git
cd StudentComplaintAnalyzer

# Step 2: Create a virtual environment
python -m venv venv

# Step 3: Activate the virtual environment
.\venv\Scripts\Activate.ps1
# (If using CMD instead of PowerShell: .\venv\Scripts\activate.bat)

# Step 4: Install required packages
pip install -r requirements.txt

# Step 5: Train the NLP Machine Learning model
python ml/train_model.py

# Step 6: Initialize and seed the database
python scripts/seed_database.py

# Step 7: Start the application
python app.py
```

Now open your browser and navigate to: **`http://127.0.0.1:5000/`**

---

## 🍎 3. Running on macOS / Linux

Open your **Terminal** and run:

```bash
# Step 1: Clone the repository
git clone https://github.com/YOUR_USERNAME/StudentComplaintAnalyzer.git
cd StudentComplaintAnalyzer

# Step 2: Create a virtual environment
python3 -m venv venv

# Step 3: Activate the virtual environment
source venv/bin/activate

# Step 4: Install required packages
pip install -r requirements.txt

# Step 5: Train the NLP Machine Learning model
python3 ml/train_model.py

# Step 6: Initialize and seed the database
python3 scripts/seed_database.py

# Step 7: Start the application
python3 app.py
```

Now open your browser and navigate to: **`http://127.0.0.1:5000/`**

---

## 🗄️ 4. Database Setup Options

The application works with **both** Supabase (Cloud PostgreSQL) and SQLite (Local Zero-Config):

### Option A: Using Supabase (Cloud Database)
1. Create a `.env` file in the project root:
   ```env
   SECRET_KEY=smartcampus-college-secret-key-2026
   FLASK_ENV=development
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres?sslmode=require
   ```
2. (Optional) Run [`supabase_schema.sql`](supabase_schema.sql) in your **Supabase SQL Editor** to populate tables in the cloud.

### Option B: Local SQLite (Zero Setup / Offline)
- Simply do **not** provide a `DATABASE_URL` in `.env` (or leave it commented out).
- The application will automatically create and use a local SQLite database at `instance/database.db`. Perfect for offline college presentations!

---

## 🧪 5. Running Automated Verification Tests

To verify that the NLP classifier, sentiment analyzer, authentication, and all routes are working properly:

```bash
pytest -v
```

All 15 test suites should pass with `100% SUCCESS`.

---

## 🛠️ Common Troubleshooting

- **Python Version**: Python 3.10, 3.11, 3.12, or 3.13 recommended.
- **PowerShell Script Execution Policy**: If PowerShell blocks `Activate.ps1`, run:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- **Port In Use**: If port 5000 is occupied, set a different port before running:
  ```powershell
  $env:PORT="5050"; python app.py
  ```
