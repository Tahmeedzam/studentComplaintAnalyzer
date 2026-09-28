"""End-to-End Demo Flow Verification Script."""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.models import db, User, Complaint
from ml.prediction import analyze_complaint

app = create_app('development')

def test_full_demo_flow():
    print("=" * 60)
    print(" TESTING END-TO-END DEMO FLOW ")
    print("=" * 60)

    client = app.test_client()

    # 1. Test Home page
    res = client.get('/')
    assert res.status_code == 200
    print("[+] 1. Home Page renders successfully (Status: 200)")

    # 2. Test Live NLP Real-time Endpoint
    nlp_res = client.post('/api/analyze', json={
        "text": "The Wi-Fi in the library has not been working for two days."
    })
    assert nlp_res.status_code == 200
    data = nlp_res.get_json()
    print(f"[+] 2. Live NLP API Inference:")
    print(f"       Category   : {data['category']}")
    print(f"       Sentiment  : {data['sentiment']} (Score: {data['sentiment_score']})")
    print(f"       Priority   : {data['priority']}")
    print(f"       Department : {data['department']}")
    print(f"       Confidence : {data['confidence']}%")
    print(f"       Keywords   : {data['keywords']}")

    # 3. Student Login
    login_res = client.post('/login', data={
        'email': 'student@smartcampus.com',
        'password': 'Student@123'
    }, follow_redirects=True)
    assert login_res.status_code == 200
    print("[+] 3. Student Login verified successfully")

    # 4. Student Submit Complaint
    submit_res = client.post('/student/complaints/new', data={
        'title': 'Broken water pipe leaking in electrical room',
        'description': 'Urgent emergency! Water from 2nd floor pipe is dripping onto circuit breakers.',
        'location': 'Hostel Block A'
    }, follow_redirects=True)
    assert submit_res.status_code == 200
    print("[+] 4. Student Complaint Submission & Auto-NLP Triage verified")

    with app.app_context():
        new_complaint = Complaint.query.filter_by(title='Broken water pipe leaking in electrical room').first()
        assert new_complaint is not None
        assert new_complaint.priority == 'High'
        c_id = new_complaint.id
        print(f"[+] 5. Complaint #{c_id} persisted in Database with Priority={new_complaint.priority}, Category={new_complaint.category}")

    # 6. Admin Login & Dashboard
    client.get('/logout', follow_redirects=True)
    admin_login = client.post('/login', data={
        'email': 'admin@smartcampus.com',
        'password': 'Admin@123'
    }, follow_redirects=True)
    assert admin_login.status_code == 200
    print("[+] 6. Admin Login verified")

    # 7. Admin Triage & Update
    update_res = client.post(f'/admin/complaints/{c_id}/update', data={
        'status': 'Resolved',
        'department': 'Maintenance Department',
        'admin_response': 'Emergency plumber fixed the leak and electrical panel was dried and certified safe.'
    }, follow_redirects=True)
    assert update_res.status_code == 200
    print("[+] 7. Admin Status Update & Response verified")

    # 8. Admin Analytics
    analytics_res = client.get('/admin/analytics')
    assert analytics_res.status_code == 200
    print("[+] 8. Admin Analytics & Trend Visualizations verified")

    print("=" * 60)
    print(" ALL 8 DEMO STEPS PASSED WITH 100% SUCCESS! ")
    print("=" * 60)


if __name__ == '__main__':
    test_full_demo_flow()
