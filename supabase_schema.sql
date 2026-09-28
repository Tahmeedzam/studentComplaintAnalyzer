-- ==============================================================================
-- SMART STUDENT COMPLAINT ANALYZER - SUPABASE POSTGRESQL SCHEMA & SEED SCRIPT
-- ==============================================================================
-- Run this SQL in your Supabase Project Dashboard:
-- 1. Open your Supabase Dashboard: https://supabase.com/dashboard/
-- 2. Go to "SQL Editor" on the left menu
-- 3. Click "New Query", paste this entire file, and click "Run"
-- ==============================================================================

-- 1. DROP EXISTING TABLES IF RE-INITIALIZING
DROP TABLE IF EXISTS complaints CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. CREATE USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student' CHECK (role IN ('student', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for high-performance user authentication lookup
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 3. CREATE COMPLAINTS TABLE
CREATE TABLE IF NOT EXISTS complaints (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(80) NOT NULL DEFAULT 'Other',
    sentiment VARCHAR(30) NOT NULL DEFAULT 'Neutral' CHECK (sentiment IN ('Positive', 'Neutral', 'Negative')),
    sentiment_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    priority VARCHAR(20) NOT NULL DEFAULT 'Low' CHECK (priority IN ('High', 'Medium', 'Low')),
    department VARCHAR(100) NOT NULL DEFAULT 'Administrative Office',
    confidence DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    keywords TEXT DEFAULT '[]',
    status VARCHAR(30) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'In Progress', 'Resolved', 'Rejected')),
    admin_response TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for dashboard filtering and querying
CREATE INDEX IF NOT EXISTS idx_complaints_student_id ON complaints(student_id);
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);
CREATE INDEX IF NOT EXISTS idx_complaints_category ON complaints(category);
CREATE INDEX IF NOT EXISTS idx_complaints_priority ON complaints(priority);
CREATE INDEX IF NOT EXISTS idx_complaints_created_at ON complaints(created_at DESC);

-- 4. AUTOMATIC UPDATED_AT TRIGGER FUNCTION
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_complaints_updated_at ON complaints;
CREATE TRIGGER trg_complaints_updated_at
BEFORE UPDATE ON complaints
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ==============================================================================
-- 5. SEED INITIAL DATA (ADMIN, STUDENTS & SAMPLE COMPLAINTS)
-- ==============================================================================

-- Insert Admin & Demo Students
-- Password for Admin: Admin@123
-- Password for Students: Student@123
INSERT INTO users (id, name, email, password_hash, role, created_at) VALUES
(1, 'Campus Administrator', 'admin@smartcampus.com', 'scrypt:32768:8:1$Lm09qWzTtIQa8dYI$fc7cae05c893d41a8a4710db417eefd69fe602120a74ff4f8000d7914e2a783bfa6b3cf36cafea1b731c3f48cd4e5bb8ac23b133fe2069c4d0c99d02f9b96176', 'admin', NOW() - INTERVAL '60 days'),
(2, 'Aarav Sharma', 'student@smartcampus.com', 'scrypt:32768:8:1$pvSkmrvzBj9urNsG$3085176a8eb41a89523766ffceb9cc9b5c5dbb0d5feb9ee7f912fd81de0fb9208ad57c630773eb7536b23810bffc024063de7a452e8c8bf408b33f83c9edd96a', 'student', NOW() - INTERVAL '50 days'),
(3, 'Priya Patel', 'priya@smartcampus.com', 'scrypt:32768:8:1$pvSkmrvzBj9urNsG$3085176a8eb41a89523766ffceb9cc9b5c5dbb0d5feb9ee7f912fd81de0fb9208ad57c630773eb7536b23810bffc024063de7a452e8c8bf408b33f83c9edd96a', 'student', NOW() - INTERVAL '45 days'),
(4, 'Rohan Verma', 'rohan@smartcampus.com', 'scrypt:32768:8:1$pvSkmrvzBj9urNsG$3085176a8eb41a89523766ffceb9cc9b5c5dbb0d5feb9ee7f912fd81de0fb9208ad57c630773eb7536b23810bffc024063de7a452e8c8bf408b33f83c9edd96a', 'student', NOW() - INTERVAL '40 days');

-- Reset users sequence to avoid collision on next registration
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- Insert Sample Complaints
INSERT INTO complaints (student_id, title, description, category, sentiment, sentiment_score, priority, department, confidence, keywords, status, admin_response, created_at, updated_at) VALUES
(2, 'Wi-Fi in Central Library is constantly disconnecting', 'The campus Wi-Fi router on the second floor of the central library has not been functioning properly for three days. Research downloads fail and students cannot attend online lab sessions.', 'IT & Wi-Fi', 'Negative', -0.42, 'High', 'IT Support', 92.5, '["Wifi", "Library", "Router", "Disconnect", "Central"]', 'Resolved', 'IT Support replaced the faulty router on the 2nd floor with a high-capacity dual-band access point. Network connectivity has been fully restored.', NOW() - INTERVAL '12 days', NOW() - INTERVAL '11 days'),

(3, 'Severe water leakage near electrical panel in Civil block', 'Urgent emergency: Rainwater is dripping directly onto the open main circuit breaker box in the 1st floor corridor of the Civil Engineering building. High risk of electrical shock and fire hazard.', 'Infrastructure', 'Negative', -0.68, 'High', 'Maintenance Department', 94.1, '["Water", "Leakage", "Electrical", "Emergency", "Hazard"]', 'Resolved', 'Emergency maintenance dispatched. The rooftop drainage pipe was sealed and the electrical panel was insulated and certified safe by campus electricians.', NOW() - INTERVAL '15 days', NOW() - INTERVAL '14 days'),

(4, 'Uncooked food served in Hostel Dining Hall', 'Yesterdays dinner in block B mess had raw chicken and contaminated water. Several hostel residents have fallen ill with severe stomach pain and food poisoning.', 'Canteen', 'Negative', -0.62, 'High', 'Canteen Management', 89.4, '["Food", "Hostel", "Dining", "Poisoning", "Dinner"]', 'In Progress', 'The canteen inspection committee inspected the kitchen premises today. The mess contractor has been issued an official penalty and strict hygienic compliance notice.', NOW() - INTERVAL '3 days', NOW() - INTERVAL '2 days'),

(2, 'Hall ticket download link crashing before final exams', 'The online examination portal throws a 500 internal server error whenever students try to download admit cards for the upcoming semester exams starting Monday.', 'Examination', 'Negative', -0.51, 'High', 'Examination Cell', 93.8, '["Hall", "Ticket", "Exam", "Portal", "Server"]', 'In Progress', 'Examination cell database team is performing emergency server capacity scaling. Direct download links have also been emailed to all affected students.', NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 day'),

(3, 'No drinking water supply on 3rd floor Classroom Block', 'The water cooler and RO purification dispenser in Block C (Classrooms 301-310) has been bone dry for four consecutive days during hot weather.', 'Classroom', 'Negative', -0.25, 'Medium', 'Administration', 85.0, '["Water", "Cooler", "Classroom", "Floor", "Block"]', 'Pending', NULL, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),

(4, 'College Bus Route 12 regularly running 45 minutes late', 'Bus route 12 consistently skips morning stops and arrives late at campus, causing morning lecture attendance penalties for over 30 students.', 'Transport', 'Negative', -0.38, 'Medium', 'Transport Department', 91.2, '["Bus", "Route", "Late", "Morning", "Transport"]', 'In Progress', 'Transport manager has contacted the route 12 driver and revised the morning departure schedule by 20 minutes to account for highway congestion.', NOW() - INTERVAL '5 days', NOW() - INTERVAL '4 days'),

(2, 'Semester tuition fee deducted twice during online payment', 'Due to a payment gateway timeout, ₹45,000 was deducted twice from my bank account. The accounts portal still shows status as pending.', 'Fees & Accounts', 'Negative', -0.35, 'High', 'Accounts Department', 95.0, '["Fee", "Tuition", "Payment", "Account", "Deducted"]', 'Pending', NULL, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),

(3, 'Classroom 204 projector display has purple discoloration and flicker', 'The ceiling projector in room 204 has a damaged VGA/HDMI cable. Visual slides during machine learning lectures cannot be read.', 'Classroom', 'Negative', -0.30, 'Medium', 'Administration', 88.6, '["Projector", "Classroom", "Display", "Cable", "Room"]', 'Resolved', 'Maintenance replaced the HDMI cable and calibrated the projector lamp on Wednesday.', NOW() - INTERVAL '18 days', NOW() - INTERVAL '17 days'),

(4, 'Delay in issuing official Bonafide and Transcripts', 'Submitted application for passport bonafide certificate 3 weeks ago. Administrative counter keeps asking me to return next week without progress.', 'Administration', 'Negative', -0.22, 'Medium', 'Administrative Office', 87.3, '["Bonafide", "Certificate", "Counter", "Administrative", "Delay"]', 'In Progress', 'Administrative officer has approved the verification. The signed document is ready for collection at Counter 4.', NOW() - INTERVAL '6 days', NOW() - INTERVAL '5 days'),

(2, 'Hostel room 214 window glass shattered during thunderstorm', 'The window pane broke during heavy winds and cold air and insects are entering the room. Need replacement urgently.', 'Hostel', 'Negative', -0.45, 'High', 'Hostel Administration', 90.1, '["Hostel", "Window", "Room", "Glass", "Replacement"]', 'Resolved', 'Carpentry team installed a new reinforced window pane and mesh screen.', NOW() - INTERVAL '22 days', NOW() - INTERVAL '21 days'),

(3, 'Stray aggressive dogs near campus sports ground', 'A pack of stray dogs has been barking aggressively at students near the indoor badminton stadium and running track after sunset.', 'Other', 'Negative', -0.54, 'Medium', 'General Administration', 82.0, '["Dog", "Stray", "Campus", "Sports", "Ground"]', 'Pending', NULL, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),

(4, 'Professor skipping core syllabus modules in Operating Systems', 'We have only covered two chapters in OS and semester end exams are scheduled in three weeks. We request extra tutorial lectures.', 'Academics', 'Neutral', 0.0, 'Medium', 'Academic Department', 92.4, '["Professor", "Syllabus", "Operating", "System", "Lecture"]', 'In Progress', 'Head of Computer Science Department discussed with faculty. Two extra weekend revision lectures have been scheduled.', NOW() - INTERVAL '8 days', NOW() - INTERVAL '7 days'),

(2, 'Request to extend central library opening hours during exam week', 'General student suggestion: The central library currently closes at 8 PM. We request keeping the reading rooms open until midnight during examination month.', 'Library', 'Positive', 0.45, 'Low', 'Library Department', 96.2, '["Library", "Hour", "Central", "Exam", "Extend"]', 'Pending', NULL, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),

(3, 'Overcharging by campus stationery photocopy vendor', 'The bookstore shop is charging ₹3 per page instead of the university approved rate of ₹1 per page for academic printouts.', 'Other', 'Negative', -0.20, 'Low', 'General Administration', 78.5, '["Photocopy", "Vendor", "Stationery", "Rate", "Price"]', 'Rejected', 'Upon review, color printouts have an approved rate card of ₹3. Black-and-white printouts remain ₹1 as per college policy.', NOW() - INTERVAL '10 days', NOW() - INTERVAL '9 days');

-- Reset complaints sequence
SELECT setval('complaints_id_seq', (SELECT MAX(id) FROM complaints));
