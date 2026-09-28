"""Database Seeder: Populates demo accounts (admin, students) and realistic complaint records."""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Insert project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.models import db, User, Complaint
from ml.prediction import analyze_complaint

app = create_app('development')


def seed_database():
    """Populate database with demo accounts and representative complaints."""
    print("=" * 60)
    print(" SMART STUDENT COMPLAINT ANALYZER - DATABASE SEEDER ")
    print("=" * 60)

    with app.app_context():
        # Drop and recreate tables for clean seed
        db.create_all()

        # Check if already seeded
        if User.query.filter_by(email='admin@smartcampus.com').first():
            print("[!] Demo data already exists. Re-seeding fresh data...")
            Complaint.query.delete()
            User.query.delete()
            db.session.commit()

        print("[*] Creating Demo Users...")
        # 1. Admin Account
        admin = User(
            name="Campus Administrator",
            email="admin@smartcampus.com",
            role="admin",
            created_at=datetime.utcnow() - timedelta(days=60)
        )
        admin.set_password("Admin@123")
        db.session.add(admin)

        # 2. Student Accounts
        student1 = User(
            name="Aarav Sharma",
            email="student@smartcampus.com",
            role="student",
            created_at=datetime.utcnow() - timedelta(days=50)
        )
        student1.set_password("Student@123")
        db.session.add(student1)

        student2 = User(
            name="Priya Patel",
            email="priya@smartcampus.com",
            role="student",
            created_at=datetime.utcnow() - timedelta(days=45)
        )
        student2.set_password("Student@123")
        db.session.add(student2)

        student3 = User(
            name="Rohan Verma",
            email="rohan@smartcampus.com",
            role="student",
            created_at=datetime.utcnow() - timedelta(days=40)
        )
        student3.set_password("Student@123")
        db.session.add(student3)

        db.session.commit()
        print(f"[+] Created Users: 1 Admin, 3 Students")

        # 3. Seed Complaints across all categories, priorities, and statuses
        seed_complaints_data = [
            # High Priority / Negative / Resolved
            {
                "student": student1,
                "title": "Wi-Fi in Central Library is constantly disconnecting",
                "description": "The campus Wi-Fi router on the second floor of the central library has not been functioning properly for three days. Research downloads fail and students cannot attend online lab sessions.",
                "status": "Resolved",
                "admin_response": "IT Support replaced the faulty router on the 2nd floor with a high-capacity dual-band access point. Network connectivity has been fully restored.",
                "days_ago": 12
            },
            {
                "student": student2,
                "title": "Severe water leakage near electrical panel in Civil block",
                "description": "Urgent emergency: Rainwater is dripping directly onto the open main circuit breaker box in the 1st floor corridor of the Civil Engineering building. High risk of electrical shock and fire hazard.",
                "status": "Resolved",
                "admin_response": "Emergency maintenance dispatched. The rooftop drainage pipe was sealed and the electrical panel was insulated and certified safe by campus electricians.",
                "days_ago": 15
            },
            {
                "student": student3,
                "title": "Uncooked food served in Hostel Dining Hall",
                "description": "Yesterday's dinner in block B mess had raw chicken and contaminated water. Several hostel residents have fallen ill with severe stomach pain and food poisoning.",
                "status": "In Progress",
                "admin_response": "The canteen inspection committee inspected the kitchen premises today. The mess contractor has been issued an official penalty and strict hygienic compliance notice.",
                "days_ago": 3
            },
            {
                "student": student1,
                "title": "Hall ticket download link crashing before final exams",
                "description": "The online examination portal throws a 500 internal server error whenever students try to download admit cards for the upcoming semester exams starting Monday.",
                "status": "In Progress",
                "admin_response": "Examination cell database team is performing emergency server capacity scaling. Direct download links have also been emailed to all affected students.",
                "days_ago": 2
            },
            {
                "student": student2,
                "title": "No drinking water supply on 3rd floor Classroom Block",
                "description": "The water cooler and RO purification dispenser in Block C (Classrooms 301-310) has been bone dry for four consecutive days during hot weather.",
                "status": "Pending",
                "admin_response": None,
                "days_ago": 1
            },
            {
                "student": student3,
                "title": "College Bus Route 12 regularly running 45 minutes late",
                "description": "Bus route 12 consistently skips morning stops and arrives late at campus, causing morning lecture attendance penalties for over 30 students.",
                "status": "In Progress",
                "admin_response": "Transport manager has contacted the route 12 driver and revised the morning departure schedule by 20 minutes to account for highway congestion.",
                "days_ago": 5
            },
            {
                "student": student1,
                "title": "Semester tuition fee deducted twice during online payment",
                "description": "Due to a payment gateway timeout, ₹45,000 was deducted twice from my bank account. The accounts portal still shows status as pending.",
                "status": "Pending",
                "admin_response": None,
                "days_ago": 4
            },
            {
                "student": student2,
                "title": "Classroom 204 projector display has purple discoloration and flicker",
                "description": "The ceiling projector in room 204 has a damaged VGA/HDMI cable. Visual slides during machine learning lectures cannot be read.",
                "status": "Resolved",
                "admin_response": "Maintenance replaced the HDMI cable and calibrated the projector lamp on Wednesday.",
                "days_ago": 18
            },
            {
                "student": student3,
                "title": "Delay in issuing official Bonafide and Transcripts",
                "description": "Submitted application for passport bonafide certificate 3 weeks ago. Administrative counter keeps asking me to return next week without progress.",
                "status": "In Progress",
                "admin_response": "Administrative officer has approved the verification. The signed document is ready for collection at Counter 4.",
                "days_ago": 6
            },
            {
                "student": student1,
                "title": "Hostel room 214 window glass shattered during thunderstorm",
                "description": "The window pane broke during heavy winds and cold air and insects are entering the room. Need replacement urgently.",
                "status": "Resolved",
                "admin_response": "Carpentry team installed a new reinforced window pane and mesh screen.",
                "days_ago": 22
            },
            {
                "student": student2,
                "title": "Stray aggressive dogs near campus sports ground",
                "description": "A pack of stray dogs has been barking aggressively at students near the indoor badminton stadium and running track after sunset.",
                "status": "Pending",
                "admin_response": None,
                "days_ago": 2
            },
            {
                "student": student3,
                "title": "Professor skipping core syllabus modules in Operating Systems",
                "description": "We have only covered two chapters in OS and semester end exams are scheduled in three weeks. We request extra tutorial lectures.",
                "status": "In Progress",
                "admin_response": "Head of Computer Science Department discussed with faculty. Two extra weekend revision lectures have been scheduled.",
                "days_ago": 8
            },
            {
                "student": student1,
                "title": "Air conditioning unit in computer laboratory 2 is blowing warm air",
                "description": "With 40 computers running, the temperature inside lab 2 exceeds 35 degrees Celsius, making practical programming sessions intolerable.",
                "status": "Resolved",
                "admin_response": "HVAC compressor coolant was refilled and AC filters were thoroughly cleaned.",
                "days_ago": 25
            },
            {
                "student": student2,
                "title": "Overcharging by campus stationery photocopy vendor",
                "description": "The bookstore shop is charging ₹3 per page instead of the university approved rate of ₹1 per page for academic printouts.",
                "status": "Rejected",
                "admin_response": "Upon review, color printouts have an approved rate card of ₹3. Black-and-white printouts remain ₹1 as per college policy.",
                "days_ago": 10
            },
            {
                "student": student3,
                "title": "Library fine calculation discrepancy for returned reference book",
                "description": "I returned the Artificial Intelligence textbook on Friday before 5 PM, but the automated RFID scanner charged an overdue fine of ₹150.",
                "status": "Resolved",
                "admin_response": "Library circulation records verified. The system timestamp anomaly was corrected and the fine was waived from the student account.",
                "days_ago": 14
            },
            {
                "student": student1,
                "title": "Hostel bathroom door latches broken in Wing C",
                "description": "Three out of five washroom cubicle doors on the second floor have broken lock latches, causing privacy concerns for residents.",
                "status": "In Progress",
                "admin_response": "New steel tower bolts have been ordered and will be installed by the hostel plumber and carpenter tomorrow.",
                "days_ago": 3
            },
            {
                "student": student2,
                "title": "Request to extend central library opening hours during exam week",
                "description": "General student suggestion: The central library currently closes at 8 PM. We request keeping the reading rooms open until midnight during examination month.",
                "status": "Pending",
                "admin_response": None,
                "days_ago": 1
            },
            {
                "student": student3,
                "title": "Broken wooden desks tearing clothes in Room 105",
                "description": "Several front-row student benches have exposed splintered wood and nails that have ripped student uniforms and bags.",
                "status": "Resolved",
                "admin_response": "Carpentry repair completed. All benches in Room 105 were sanded and varnished.",
                "days_ago": 28
            },
            {
                "student": student1,
                "title": "Revaluation results for Mathematics III not updated on portal",
                "description": "Re-totaling result was approved by the board last month, but the official grade sheet on student portal still displays old internal marks.",
                "status": "In Progress",
                "admin_response": "Controller of Examinations has forwarded the corrected marksheet to the ERP database administrator for update.",
                "days_ago": 7
            },
            {
                "student": student2,
                "title": "Gymnasium treadmill cable snapped and weights scattered",
                "description": "Safety concern in the campus fitness center: The running belt on the main treadmill is slipping and wire pulley is frayed. It could cause serious student injury.",
                "status": "Pending",
                "admin_response": None,
                "days_ago": 2
            },
            {
                "student": student3,
                "title": "Late night loud music near hostel blocks D and E",
                "description": "Continuous loud music and celebrations past 1 AM in the guest house lawn are disturbing student sleep and exam preparations.",
                "status": "Resolved",
                "admin_response": "Campus security has enforced a strict 10 PM sound curfew across all open areas.",
                "days_ago": 16
            },
            {
                "student": student1,
                "title": "Scholarship disbursement delayed for merit students",
                "description": "The institutional fee waiver for semester toppers has not been credited to our bank accounts even though the academic year is half over.",
                "status": "In Progress",
                "admin_response": "Accounts department is reconciling treasury clearance. Disbursement will be credited within 7 business days.",
                "days_ago": 9
            }
        ]

        print(f"[*] Processing and NLP analyzing {len(seed_complaints_data)} sample complaints...")
        for item in seed_complaints_data:
            full_text = f"{item['title']}. {item['description']}"
            analysis = analyze_complaint(full_text)

            created_time = datetime.utcnow() - timedelta(days=item['days_ago'], hours=item.get('hours', 2))
            updated_time = created_time + timedelta(hours=6) if item['status'] != 'Pending' else created_time

            complaint = Complaint(
                student_id=item['student'].id,
                title=item['title'],
                description=item['description'],
                category=analysis['category'],
                sentiment=analysis['sentiment'],
                sentiment_score=analysis['sentiment_score'],
                priority=analysis['priority'],
                department=analysis['department'],
                confidence=analysis['confidence'],
                status=item['status'],
                admin_response=item['admin_response'],
                created_at=created_time,
                updated_at=updated_time
            )
            complaint.set_keywords(analysis['keywords'])
            db.session.add(complaint)

        db.session.commit()
        print(f"[+] Successfully seeded {len(seed_complaints_data)} complaints into the database!")

        print("\n" + "=" * 60)
        print(" DEMO CREDENTIALS ")
        print("=" * 60)
        print(" Administrator Account:")
        print("   Email    : admin@smartcampus.com")
        print("   Password : Admin@123\n")
        print(" Student Account:")
        print("   Email    : student@smartcampus.com")
        print("   Password : Student@123\n")
        print(" Additional Students:")
        print("   priya@smartcampus.com / Student@123")
        print("   rohan@smartcampus.com / Student@123")
        print("=" * 60)


if __name__ == '__main__':
    seed_database()
