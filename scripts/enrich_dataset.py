"""Dataset expander to ensure robust training coverage across all 12 college categories."""

import pandas as pd

additional_samples = [
    # Academics
    ("The professor for compiler design is not providing notes or lecture slides on the course portal.", "Academics"),
    ("Machine learning practical lab sessions are rushed and students are unable to execute python code.", "Academics"),
    ("Our assigned faculty guide is constantly unavailable for final year project guidance.", "Academics"),
    ("The chemistry department has not scheduled makeup classes for missed lab sessions.", "Academics"),
    ("Elective subject selection portal closed early and students were assigned random subjects.", "Academics"),
    ("Faculty member refuses to clarify mathematical proofs during lecture office hours.", "Academics"),
    ("Course syllabus for data structures is not aligned with modern industry standards.", "Academics"),
    ("The teaching assistant grading our programming homework gave zero feedback or rubrics.", "Academics"),
    ("Textbooks listed in the academic syllabus are completely unavailable in bookstores.", "Academics"),
    ("Class lecture was canceled at the last minute without any notification email to students.", "Academics"),
    ("Attendance records were uploaded incorrectly for engineering mechanics course.", "Academics"),
    ("Physics lecture speed is excessively fast making it impossible to take down notes.", "Academics"),

    # Examination
    ("The examination hall ticket portal is not allowing students to download admit cards.", "Examination"),
    ("Semester final examination schedule has three core engineering papers without any study break.", "Examination"),
    ("Revaluation and re-totaling results from last semester are delayed by four months.", "Examination"),
    ("There was a severe printing defect and missing questions in today's calculus question paper.", "Examination"),
    ("Invigilator in exam room 204 was constantly talking loudly on phone during the exam.", "Examination"),
    ("Online examination portal crashed during my test submission and marked me absent.", "Examination"),
    ("Admit card contains an error in student name and registration roll number.", "Examination"),
    ("Exam center allocated for semester end exam is located in an inaccessible area.", "Examination"),
    ("The supplementary examination fee payment receipt was not generated after deduction.", "Examination"),
    ("Evaluation of thermodynamics semester paper was unfair and inconsistent.", "Examination"),
    ("The university results portal has been down with server 500 error since morning.", "Examination"),
    ("Graduation degree certificates and final marks transcripts have not been issued.", "Examination"),

    # IT & Wi-Fi
    ("Campus Wi-Fi connectivity in the engineering block is completely dead today.", "IT & Wi-Fi"),
    ("Unable to log in to university email account due to multi-factor authentication SMS failure.", "IT & Wi-Fi"),
    ("Computer lab 4 desktop workstations have broken mice and missing ethernet cables.", "IT & Wi-Fi"),
    ("The college portal and LMS website are displaying SSL certificate security warnings.", "IT & Wi-Fi"),
    ("Internet speed across campus is severely throttled to under 50 kbps.", "IT & Wi-Fi"),
    ("Projector in seminar hall is not detecting HDMI signal from presenter laptops.", "IT & Wi-Fi"),
    ("The student ERP mobile application crashes on startup on Android and iOS.", "IT & Wi-Fi"),
    ("Firewall on college Wi-Fi is blocking academic research repositories and GitHub.", "IT & Wi-Fi"),
    ("Biometric attendance fingerprint machine at the main department gate is unresponsive.", "IT & Wi-Fi"),
    ("Printers in the central computer lab are out of toner and paper cartridges.", "IT & Wi-Fi"),
    ("Wi-Fi router in the library study lounge keeps dropping connection every few minutes.", "IT & Wi-Fi"),
    ("Virtual machine licenses for cloud computing lab have expired on university servers.", "IT & Wi-Fi"),

    # Infrastructure
    ("Severe ceiling water leakage in the civil building corridor near the power box.", "Infrastructure"),
    ("Elevator in the main academic building has been broken and non-functional for two weeks.", "Infrastructure"),
    ("Main staircase metal railing is loose and poses an immediate falling risk.", "Infrastructure"),
    ("Drinking water purifiers on the second floor are dispensing dirty muddy water.", "Infrastructure"),
    ("Street lights along the hostel road are pitch dark causing major student safety concerns.", "Infrastructure"),
    ("Fire extinguishers in the science wing have expired inspection tags.", "Infrastructure"),
    ("Large hazardous potholes at the main vehicle entrance gate have caused bike accidents.", "Infrastructure"),
    ("Restrooms on the third floor have broken flush tanks and no water supply.", "Infrastructure"),
    ("Overflowing sewage drainage near the cafeteria is generating an unbearable stench.", "Infrastructure"),
    ("Wheelchair accessibility ramp at the auditorium entrance is broken and unsafe.", "Infrastructure"),
    ("Frequent power cuts in academic block B with no generator backup kicking in.", "Infrastructure"),
    ("Loose electrical wires hanging from the ceiling in the central mechanical workshop.", "Infrastructure"),

    # Classroom
    ("The ceiling fan in room 305 is wobbling violently at high speed and might fall.", "Classroom"),
    ("Air conditioning unit in lecture hall 102 has stopped cooling and room is suffocating.", "Classroom"),
    ("Whiteboard in classroom 204 is severely scratched and marker text cannot be seen.", "Classroom"),
    ("Wooden benches in room 108 have broken planks with sharp edges tearing student clothes.", "Classroom"),
    ("Audio microphone in amphitheater lecture room produces terrible whistling feedback.", "Classroom"),
    ("Classroom 201 has broken window blinds allowing blinding sunlight on projector screen.", "Classroom"),
    ("Classroom door lock in room 402 is jammed and students got stuck inside after class.", "Classroom"),
    ("Insufficient number of chairs in room 212 forcing students to stand during lectures.", "Classroom"),
    ("Fluorescent tube lights in room 304 are flickering constantly causing eye strain.", "Classroom"),
    ("Acoustic echo in room 502 makes the teacher's voice completely unintelligible.", "Classroom"),
    ("Classroom garbage bins are overflowing with trash and haven't been emptied.", "Classroom"),
    ("Power sockets near student desks in room 301 are burnt out and dead.", "Classroom"),

    # Library
    ("The central library has insufficient copies of prescribed engineering textbooks.", "Library"),
    ("Library quiet reading room is very noisy because staff does not enforce silence.", "Library"),
    ("Online library catalog OPAC system is down and does not show book shelf locations.", "Library"),
    ("Automated RFID book checkout scanner at library desk is broken creating long lines.", "Library"),
    ("Air conditioning in the reference section on the 2nd floor of library is not turned on.", "Library"),
    ("Latest editions of scientific journals and IEEE magazines have not arrived.", "Library"),
    ("Books in computer science aisle are misplaced and scattered in other racks.", "Library"),
    ("Digital library computers have broken headphones and missing mouse pads.", "Library"),
    ("Library operating hours are too limited and should be open until midnight during exams.", "Library"),
    ("E-book portal requires on-campus IP and cannot be accessed from student homes.", "Library"),
    ("Library study cubicles lack power charging points for study laptops.", "Library"),
    ("Excessive overdue fine was charged for library books that were already returned.", "Library"),

    # Canteen
    ("Food served in the college mess is unhygienic and vegetables were half-cooked.", "Canteen"),
    ("Found insects in the lunch meal served at the central cafeteria today.", "Canteen"),
    ("Canteen snack stall is charging prices higher than the printed MRP.", "Canteen"),
    ("Cafeteria drinking water glasses and trays are greasy and poorly cleaned.", "Canteen"),
    ("The canteen menu completely lacks healthy meal and fresh juice choices.", "Canteen"),
    ("Huge crowd and 40 minute wait times at lunch counter due to single cashier.", "Canteen"),
    ("Mess food quality has deteriorated drastically over the past month.", "Canteen"),
    ("Canteen kitchen workers do not wear hygienic hairnets or gloves while cooking.", "Canteen"),
    ("Expired packaged yogurt and stale sandwiches were sold at the cafeteria counter.", "Canteen"),
    ("Dining tables in the canteen are not wiped between meals and stay messy.", "Canteen"),
    ("Canteen counter does not accept digital UPI or card payments.", "Canteen"),
    ("Multiple students suffered food poisoning after eating cafeteria chicken meal.", "Canteen"),

    # Hostel
    ("Hot water geysers in hostel block C are broken during freezing cold weather.", "Hostel"),
    ("Severe water shortage in boys hostel A with zero water supply in morning.", "Hostel"),
    ("Hostel room allocated to me has severe bed bug problem and damp leaking walls.", "Hostel"),
    ("Hostel Wi-Fi router is turned off every night at 10 PM stopping exam prep.", "Hostel"),
    ("Hostel security guards allow unauthorized outsiders into the student block.", "Hostel"),
    ("Washroom drains on 2nd floor of girls hostel are clogged with foul water backing up.", "Hostel"),
    ("Hostel drinking water dispenser filter has brown rust and dirt sediments.", "Hostel"),
    ("Hostel warden refuses to sign student leave and outstation permission slips.", "Hostel"),
    ("Hostel gymnasium equipment has frayed steel cables and rusted weights.", "Hostel"),
    ("Electricity voltage spikes in hostel rooms have damaged laptop power adapters.", "Hostel"),
    ("Hostel washing machines in laundry room are broken and not spinning.", "Hostel"),
    ("Hostel room door lock latch is loose and can be pushed open without key.", "Hostel"),

    # Transport
    ("College bus route 8 arrives 35 minutes late every morning causing missed classes.", "Transport"),
    ("University transit bus is severely overcrowded with students standing on footboard.", "Transport"),
    ("Bus driver on route 14 was driving dangerously fast and using phone while driving.", "Transport"),
    ("Air conditioning on the college transport bus is non-functional with windows sealed.", "Transport"),
    ("Student bus pass renewal process takes over two weeks of administrative delays.", "Transport"),
    ("Campus shuttle bus frequency between engineering and medical blocks is too low.", "Transport"),
    ("Bus broke down on the expressway and no replacement transport was sent for hours.", "Transport"),
    ("College bus seats have torn fabric with metal springs poking out.", "Transport"),
    ("Bus skipped the designated bus pickup stop leaving 15 students stranded.", "Transport"),
    ("No evening college bus service available for students staying late for lab projects.", "Transport"),
    ("Two-wheeler vehicle parking area has no security guard and helmet theft is frequent.", "Transport"),
    ("College bus live GPS location tracking application is completely inaccurate.", "Transport"),

    # Administration
    ("Administrative office staff is unhelpful, rude, and closes query counters early.", "Administration"),
    ("Application for duplicate college identity card has been pending for six weeks.", "Administration"),
    ("No proper guidance provided for obtaining official college bonafide certificate.", "Administration"),
    ("Huge unorganized queues at administration building with no token queuing system.", "Administration"),
    ("Administrative office misplaced my original submitted migration and transfer certificates.", "Administration"),
    ("Staff at admin window took a two hour lunch break while students waited outside.", "Administration"),
    ("Correction of father name in university database is pending despite submitting affidavit.", "Administration"),
    ("Official university helpline telephone numbers are never answered by operators.", "Administration"),
    ("Scholarship application notification was posted on notice board after the deadline.", "Administration"),
    ("Security guards at campus main gate treat students disrespectfully.", "Administration"),
    ("Student grievance redressal portal requests are closed without any resolution.", "Administration"),
    ("Administrative counter refused to provide an acknowledgement slip for received form.", "Administration"),

    # Fees & Accounts
    ("Semester tuition fee was debited twice from my bank account due to portal glitch.", "Fees & Accounts"),
    ("Late fee fine was charged unfairly although payment was attempted before deadline.", "Fees & Accounts"),
    ("Government scholarship funds have not been disbursed to my student bank account.", "Fees & Accounts"),
    ("Accounts department has not updated my semester fee payment status on ERP portal.", "Fees & Accounts"),
    ("No itemized receipt or breakdown is provided for miscellaneous activity fees.", "Fees & Accounts"),
    ("Security caution deposit refund cheque bounced due to accounts officer signature error.", "Fees & Accounts"),
    ("Fee installment request was rejected without evaluating genuine financial hardship.", "Fees & Accounts"),
    ("Accounts office refuses online net banking and demands physical bank demand drafts.", "Fees & Accounts"),
    ("Incorrect fine of 1500 rupees was added to fee portal for nonexistent library dues.", "Fees & Accounts"),
    ("Hostel fee refund for vacating early during semester has been delayed for months.", "Fees & Accounts"),
    ("Payment gateway charges an exorbitant convenience fee on debit card payments.", "Fees & Accounts"),
    ("Merit scholarship fee concession was not credited to my semester fee voucher.", "Fees & Accounts"),

    # Other
    ("Pack of aggressive stray dogs chasing students near the campus sports ground.", "Other"),
    ("Gymnasium treadmill and workout machines are broken with cables dangling dangerously.", "Other"),
    ("Sanitary napkin vending machines in ladies washrooms are empty and unmaintained.", "Other"),
    ("Heavy smoke from burning garden dry leaves behind the playground causes breathing problems.", "Other"),
    ("Campus bookstore overcharges students on standard stationary and lab notebooks.", "Other"),
    ("Lack of wheelchair ramps and tactile paths for physically disabled students.", "Other"),
    ("Campus medical dispensary does not have basic first aid or fever medicines.", "Other"),
    ("Loud noise and music from adjacent marriage hall disturbs student night study.", "Other"),
    ("College cricket pitch and sports ground are overgrown with weeds and muddy puddles.", "Other"),
    ("Campus ambulance has a flat tire and is parked out of commission.", "Other"),
    ("Mosquito fogging has not been carried out leading to mosquito breeding on campus.", "Other"),
    ("First aid emergency kit in indoor sports stadium is completely empty.", "Other"),
]

existing_df = pd.read_csv('data/complaints_dataset.csv')
new_df = pd.DataFrame(additional_samples, columns=['text', 'category'])
combined_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates(subset=['text'])

combined_df.to_csv('data/complaints_dataset.csv', index=False)
print(f"Total dataset samples after enrichment: {len(combined_df)}")
