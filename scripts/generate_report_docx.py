"""Script to generate the complete academic project report in NLP_MINI_PROJECT_FINALL.docx."""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    """Set shading background color for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set padding/margins for table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def generate_report():
    doc = docx.Document()

    # Set document margins (1 inch around)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # 1. Main Project Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("Smart Student Complaint Analyzer\nAn Automated NLP and Machine Learning System for Campus Grievance Redressal")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    p_title.paragraph_format.space_after = Pt(14)

    # 2. Team Members Box
    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_team_label = p_team.add_run("PROJECT REPORT BY:\n")
    r_team_label.font.bold = True
    r_team_label.font.size = Pt(11)
    r_team_label.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    team_members = [
        ("Tahmeed Zamindar", "242P003"),
        ("Moin Qureshi", "231P120"),
        ("Chinmay Sawant", "231P108")
    ]
    for name, roll in team_members:
        r_member = p_team.add_run(f"• {name} — Roll No: {roll}\n")
        r_member.font.size = Pt(11)
        r_member.font.bold = True
        r_member.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    p_team.paragraph_format.space_after = Pt(20)

    def add_section_heading(title_text):
        h = doc.add_paragraph()
        r = h.add_run(title_text)
        r.font.name = 'Calibri'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        return h

    def add_body_paragraph(text):
        p = doc.add_paragraph(text)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        return p

    # 3. Abstract
    add_section_heading("1. Abstract")
    add_body_paragraph(
        "In modern higher educational institutions, students frequently encounter academic, administrative, and infrastructural challenges that require timely resolution. Traditional manual grievance redressal mechanisms suffer from prolonged response latencies, subjective triage, and misrouting across decentralized campus administrative units. The Smart Student Complaint Analyzer is an automated, end-to-end full-stack Natural Language Processing (NLP) web application designed to streamline student grievance management. The system leverages text normalization, WordNet lemmatization, and TF-IDF n-gram vectorization coupled with a Multinomial Logistic Regression / Linear SVM classifier to accurately categorize unstructured student text across 12 distinct campus departments. Furthermore, it incorporates NLTK VADER sentiment analysis to gauge grievance severity and applies rule-based heuristic logic to dynamically assign urgency priorities (High, Medium, Low). Built upon Python, Flask, Supabase PostgreSQL, and Bootstrap 5, the platform delivers automated triage, executive analytics, and lifecycle tracking, offering a robust, transparent, and scalable solution for campus administration."
    )

    # 4. Problem Statement & Motivation
    add_section_heading("2. Problem Statement & Motivation")
    add_body_paragraph(
        "Educational institutions manage thousands of students daily across diverse domains such as examinations, information technology, laboratory equipment, hostels, transportation, and cafeteria operations. When students submit complaints, administration teams face critical bottlenecks:"
    )
    bullet_points_prob = [
        ("Manual Sorting Overhead: ", "Administrative personnel must read every ticket to identify the responsible department, creating multi-day communication backlogs."),
        ("Lack of Urgency Prioritization: ", "Critical safety hazards (e.g., electrical sparking, water leakages, examination portal timeouts) are often queued sequentially with minor suggestions."),
        ("No Sentiment or Keyword Visibility: ", "Institutions lack automated sentiment monitoring to detect widespread student distress or recurring infrastructure failures."),
        ("Opaque Tracking: ", "Students lack visibility into whether their complaint is under review, assigned to a technician, or resolved.")
    ]
    for b_title, b_desc in bullet_points_prob:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(b_title)
        r1.bold = True
        p.add_run(b_desc)
        p.paragraph_format.space_after = Pt(3)

    # 5. Objectives
    add_section_heading("3. Objectives")
    objectives = [
        "To develop an intelligent NLP classification pipeline that automatically categorizes unstructured complaint text into 12 predefined institutional categories with high precision.",
        "To perform real-time sentiment polarity analysis (Positive, Neutral, Negative) using VADER to quantify the emotional intensity and tone of student feedback.",
        "To implement a dynamic priority scoring engine that detects emergency and hazard keywords, assigning High, Medium, or Low urgency levels.",
        "To extract key representative domain keywords and acronyms (e.g., AC, Wi-Fi, OPAC, ERP) to provide instant contextual summaries for department heads.",
        "To build a responsive, production-ready web application featuring role-based access control (Student Portal & Admin Dashboard), Chart.js visual analytics, and Supabase cloud PostgreSQL storage."
    ]
    for obj in objectives:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(obj)
        p.paragraph_format.space_after = Pt(3)

    # 6. Technology Stack & Tools Used
    add_section_heading("4. Technology Stack & Tools Used")
    tech_table = doc.add_table(rows=1, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.autofit = False

    hdr_cells = tech_table.rows[0].cells
    hdr_titles = ["Component / Layer", "Technology / Library", "Key Responsibility"]
    col_widths = [Inches(1.8), Inches(2.2), Inches(2.5)]

    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i])
        hdr_cells[i].width = col_widths[i]

    tech_data = [
        ("Programming Language", "Python 3.11+", "Core backend, NLP pipeline, and machine learning execution"),
        ("Web Framework", "Flask 3.0 & Flask-Login", "Application routing, session management, and RBAC authentication"),
        ("NLP & Text Processing", "NLTK 3.8+", "Tokenization, stopword removal, WordNet lemmatization, VADER sentiment"),
        ("Machine Learning", "Scikit-Learn & Joblib", "TF-IDF vectorizer, Multinomial Logistic Regression, model persistence"),
        ("Database Layer", "Supabase PostgreSQL / SQLite", "Relational database schema, SQLAlchemy ORM, and cloud persistence"),
        ("Frontend UI", "HTML5, CSS3, Bootstrap 5.3", "Responsive student and administrative portals with light institutional theme"),
        ("Data Visualization", "Chart.js 4.4+", "Dynamic interactive analytics charts (Category, Sentiment, Priority, Trends)"),
        ("Testing Framework", "Pytest 8.0+", "Automated unit and integration test suites for NLP and web routes")
    ]

    for row_idx, data in enumerate(tech_data):
        row_cells = tech_table.add_row().cells
        bg_color = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for i, val in enumerate(data):
            row_cells[i].text = val
            row_cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_background(row_cells[i], bg_color)
            set_cell_margins(row_cells[i])
            row_cells[i].width = col_widths[i]

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 7. Dataset Description
    add_section_heading("5. Dataset Description")
    add_body_paragraph(
        "A customized, balanced dataset comprising 496 authentic college grievances was curated across 12 distinct functional categories. Each complaint sample contains realistic phrasing, campus acronyms, contractions, and varying levels of emotional tone representing everyday student scenarios."
    )
    categories_list = [
        ("Academics: ", "Syllabus completion, professor availability, grading transparency, project guides."),
        ("Examination: ", "Hall tickets, admit card download errors, revaluation delays, exam schedule overlaps."),
        ("IT & Wi-Fi: ", "Wi-Fi disconnections, student portal downtime, lab PC defects, email password lockouts."),
        ("Infrastructure: ", "Water leaks, broken elevator, power cuts, hazardous potholes, fire extinguishers."),
        ("Classroom: ", "AC cooling failures, wobbling ceiling fans, broken student benches, stained whiteboards."),
        ("Library: ", "Textbook shortages, reading room noise, OPAC catalog errors, RFID checkout scanners."),
        ("Canteen: ", "Food quality, hygiene violations, overcharging above MRP, lunch counter queues."),
        ("Hostel: ", "Geyser malfunctions, water shortages, bed bug infestations, curfew timing restrictions."),
        ("Transport: ", "Bus route delays, overcrowding, reckless driving, GPS tracking discrepancies."),
        ("Administration: ", "ID card re-issuance delays, bonafide certificates, staff counter availability."),
        ("Fees & Accounts: ", "Double deductions on gateway, late fee disputes, scholarship disbursement delays."),
        ("Other: ", "Campus stray animals, gym equipment maintenance, sanitary dispensers, environmental hygiene.")
    ]
    for c_name, c_desc in categories_list:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(c_name)
        r.bold = True
        p.add_run(c_desc)
        p.paragraph_format.space_after = Pt(2)

    # 8. NLP Pipeline & Methodology
    add_section_heading("6. NLP Pipeline & Methodology")
    add_body_paragraph(
        "The Natural Language Processing pipeline transforms unstructured text input through a rigorous sequence of linguistic transformations and statistical learning models:"
    )

    nlp_steps = [
        ("1. Acronym & Contraction Normalization: ", "Conversational contractions (e.g., \"there's\" -> \"there is\", \"don't\" -> \"do not\") and campus acronyms (e.g., \"AC\" -> \"ac air conditioning\", \"Wi-Fi\" -> \"wifi internet\", \"lab\" -> \"laboratory\") are expanded to eliminate out-of-vocabulary mismatches."),
        ("2. Text Cleaning & Noise Filtering: ", "Lowercases text and removes URLs, email addresses, non-alphanumeric punctuation, and excessive whitespace."),
        ("3. Tokenization & Stop Word Removal: ", "Splits text into discrete word tokens using NLTK word_tokenize. Custom domain stop words (e.g., \"please\", \"kindly\", \"sir\") are removed while preserving crucial short tokens (e.g., 'ac', 'os', 'ai', 'ml')."),
        ("4. Morphological Lemmatization: ", "Utilizes WordNetLemmatizer to reduce morphological inflections to root dictionary headwords (e.g., 'disconnecting' -> 'disconnect', 'leaking' -> 'leak')."),
        ("5. TF-IDF Feature Representation: ", "Extracts unigram and bigram features with sublinear term-frequency scaling to weight informative tokens inversely against corpus frequency."),
        ("6. Supervised Classification: ", "A calibrated Multinomial Logistic Regression classifier evaluates class probabilities via the Softmax function, yielding both the predicted category and a true percentage confidence score."),
        ("7. Sentiment Intensity Analysis: ", "NLTK VADER computes compound polarity scores (-1.0 to +1.0) with domain-specific deficiency heuristics ensuring facility faults correctly register as negative."),
        ("8. Smart Priority Engine: ", "Evaluates hazard lexicon terms (emergency, fire, spark, medical, food poisoning) combined with negative polarity to compute High, Medium, or Low priority."),
        ("9. Keyphrase Extraction: ", "Extracts top-ranking descriptive tokens as badge tags for executive summary display.")
    ]

    for s_title, s_desc in nlp_steps:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(s_title)
        r.bold = True
        p.add_run(s_desc)
        p.paragraph_format.space_after = Pt(3)

    # 9. Experimental Evaluation & Benchmark Results
    add_section_heading("7. Experimental Evaluation & Benchmark Results")
    add_body_paragraph(
        "To validate the optimal machine learning algorithm for college complaint classification, four candidate supervised learning algorithms were benchmarked on a stratified 80/20 train-test split:"
    )

    eval_table = doc.add_table(rows=1, cols=5)
    eval_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eval_table.autofit = False

    eval_hdrs = ["Model / Algorithm", "Accuracy", "Precision", "Recall", "F1-Score"]
    eval_widths = [Inches(2.5), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)]

    for i, title in enumerate(eval_hdrs):
        eval_table.rows[0].cells[i].text = title
        eval_table.rows[0].cells[i].paragraphs[0].runs[0].font.bold = True
        eval_table.rows[0].cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(eval_table.rows[0].cells[i], "1B365D")
        set_cell_margins(eval_table.rows[0].cells[i])
        eval_table.rows[0].cells[i].width = eval_widths[i]

    eval_data = [
        ("Multinomial Naive Bayes", "78.72%", "79.51%", "78.72%", "78.16%"),
        ("Logistic Regression (Selected)", "82.98%", "84.21%", "82.98%", "82.73%"),
        ("Linear SVM (LinearSVC)", "84.04%", "85.38%", "84.04%", "83.93%"),
        ("Random Forest Classifier", "75.53%", "79.60%", "75.53%", "75.61%")
    ]

    for row_idx, data in enumerate(eval_data):
        row_cells = eval_table.add_row().cells
        bg_color = "EFF6FF" if "Selected" in data[0] else ("F8FAFC" if row_idx % 2 == 0 else "FFFFFF")
        for i, val in enumerate(data):
            row_cells[i].text = val
            row_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
            if "Selected" in data[0]:
                row_cells[i].paragraphs[0].runs[0].font.bold = True
            set_cell_background(row_cells[i], bg_color)
            set_cell_margins(row_cells[i])
            row_cells[i].width = eval_widths[i]

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_body_paragraph(
        "Logistic Regression and Linear SVM demonstrated superior balanced precision and generalization across all 12 categories, with Logistic Regression chosen as the core engine due to its calibrated probability output enabling confidence percentage visualization."
    )

    # 10. Screenshots & Visual Outputs (Blank Space for User)
    add_section_heading("8. System Outputs & Screenshots")
    add_body_paragraph(
        "Below are the visual screenshots demonstrating the operational workflow of the Smart Student Complaint Analyzer, including student grievance submission with real-time NLP analysis, administrative triage, and institutional analytics:"
    )

    # Output boxes with clear dotted/framed borders and labels for student to paste images
    screenshot_slots = [
        ("Figure 8.1: Student Complaint Submission Page with Real-Time NLP Pre-Analysis Preview", 2.8),
        ("Figure 8.2: Student Grievance Tracking Timeline and NLP Breakdown Card", 2.8),
        ("Figure 8.3: Administrative Command Center & Complaint Management Table", 2.8),
        ("Figure 8.4: Institutional Analytics Dashboard (Category, Sentiment, Priority & Trends)", 2.8)
    ]

    for caption, height_in in screenshot_slots:
        # Create a container box table
        box_table = doc.add_table(rows=1, cols=1)
        box_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        box_table.autofit = False
        cell = box_table.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=200, bottom=200, left=200, right=200)

        p_box = cell.paragraphs[0]
        p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_box = p_box.add_run("\n\n[ PASTE SCREENSHOT HERE ]\n\n")
        r_box.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
        r_box.font.bold = True
        r_box.font.size = Pt(12)

        # Caption
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run(caption)
        r_cap.font.size = Pt(10)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        p_cap.paragraph_format.space_after = Pt(16)

    # 11. Conclusion & Future Scope
    add_section_heading("9. Conclusion & Future Scope")
    add_body_paragraph(
        "The Smart Student Complaint Analyzer successfully bridges the gap between students and campus administration by eliminating manual ticket triage. By integrating TF-IDF vectorization, Logistic Regression classification, and VADER sentiment scoring within a responsive web application, the system delivers sub-second automated categorization, prioritization, and routing. The platform promotes transparency, accountability, and accelerated grievance resolution."
    )
    add_body_paragraph(
        "Future enhancements include expanding multi-lingual support for regional languages using IndicBERT transformer models, introducing automated SMS/Email notifications on status updates, and integrating Computer Vision algorithms for automated optical verification of broken infrastructure images."
    )

    # 12. References
    add_section_heading("10. References")
    refs = [
        "Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit. O'Reilly Media.",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "Hutto, C., & Gilbert, E. (2014). VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text. Proceedings of the International AAAI Conference on Web and Social Media, 8(1), 216-225.",
        "Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python. O'Reilly Media.",
        "Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press."
    ]
    for ref in refs:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(ref)
        p.paragraph_format.space_after = Pt(3)

    # Save to the existing docx file
    doc.save('NLP_MINI_PROJECT_FINALL.docx')
    print("Report successfully generated into NLP_MINI_PROJECT_FINALL.docx")

if __name__ == '__main__':
    generate_report()
