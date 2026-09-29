"""Update NLP_MINI_PROJECT_FINALL.docx in-place adhering strictly to the original document format."""

import docx

def update_report_in_place():
    doc = docx.Document('NLP_MINI_PROJECT_FINALL.docx')

    # Mapping of paragraph content replacements
    # Title & Header
    doc.paragraphs[0].text = "Smart Student Complaint Analyzer"
    
    # Title Section & Team Members
    doc.paragraphs[3].text = "Title & Team Members"
    doc.paragraphs[4].text = (
        "Smart Student Complaint Analyzer: An Automated Natural Language Processing and Machine Learning System for Campus Grievance Redressal\n\n"
        "Team Members:\n"
        "• Tahmeed Zamindar - 242P003\n"
        "• Moin Qureshi - 231P120\n"
        "• Chinmay Sawant - 231P108"
    )

    # Abstract
    doc.paragraphs[6].text = "Abstract"
    doc.paragraphs[7].text = (
        "Smart Student Complaint Analyzer is a real-world Natural Language Processing (NLP) and Machine Learning mini project designed to automate the categorization, prioritization, and routing of student grievances in educational institutions. The system analyzes raw, unstructured complaint text using text preprocessing, WordNet lemmatization, and TF-IDF feature extraction combined with a trained classification model. It accurately classifies complaints across 12 distinct campus categories (such as Academics, IT & Wi-Fi, Examination, Classroom, Hostel, and Canteen), performs sentiment polarity scoring using NLTK VADER, and calculates urgency priority (High, Medium, Low) based on grievance deficiency patterns and safety keywords. The application provides a clean web interface for students to submit and track issues, along with an administrative dashboard and analytics."
    )

    # Problem Statement
    doc.paragraphs[9].text = "Problem Statement"
    doc.paragraphs[10].text = (
        "In universities and colleges, students submit hundreds of complaints across various academic and infrastructure departments. Traditional manual sorting of complaints is time-consuming, prone to human error, and often results in delays for urgent issues such as electrical hazards, examination portal timeouts, or water shortages. The objective of Smart Student Complaint Analyzer is to provide an automated NLP-based solution that accepts natural-language complaint text, classifies it into the appropriate department, detects emotional sentiment, assigns priority levels, and extracts key terms to streamline campus administration and accelerate issue resolution."
    )

    # Tools & Libraries Used
    doc.paragraphs[12].text = "Tools & Libraries Used"
    doc.paragraphs[13].text = (
        "Python was used for the complete implementation. Flask and Flask-Login were utilized to build the backend server, user authentication, and web routes. Natural Language Toolkit (NLTK) was used for tokenization, stop-word removal, WordNet lemmatization, and VADER sentiment intensity analysis. Scikit-Learn was used for TF-IDF vectorization and machine learning classification (Multinomial Logistic Regression and Linear SVM). SQLAlchemy ORM was configured to manage database operations with Supabase PostgreSQL and local SQLite fallback. Bootstrap 5, Bootstrap Icons, Vanilla JavaScript, and Chart.js were used for building the responsive frontend UI and analytics charts."
    )

    # Dataset Description
    doc.paragraphs[15].text = "Dataset Description"
    doc.paragraphs[16].text = (
        "The project utilizes a curated, balanced dataset of 496 realistic college complaint samples distributed across 12 campus categories: Academics, Examination, IT & Wi-Fi, Infrastructure, Classroom, Library, Canteen, Hostel, Transport, Administration, Fees & Accounts, and Other. The dataset includes common student phrasing, contractions, and campus-specific acronyms (such as AC, Wi-Fi, OPAC, and ERP). Each sample is labeled with its corresponding category to facilitate supervised machine learning classification."
    )

    # Preprocessing Techniques
    doc.paragraphs[18].text = "Preprocessing Techniques"
    doc.paragraphs[19].text = (
        "The input text undergoes a multi-stage NLP preprocessing pipeline before feature extraction and inference. Key preprocessing steps include: (1) contraction and campus acronym normalization (e.g., expanding 'AC' to 'ac air conditioning' and 'Wi-Fi' to 'wifi internet'), (2) lowercase conversion, (3) removal of URLs, email addresses, and non-alphanumeric punctuation, (4) tokenization using NLTK word_tokenize, (5) removal of standard English and domain-specific conversational stop-words while preserving meaningful short tokens (e.g., 'ac', 'os', 'ai', 'ml'), and (6) morphological lemmatization using WordNetLemmatizer to reduce inflected words to their root forms."
    )

    # Model Development
    doc.paragraphs[21].text = "Model Development"
    doc.paragraphs[22].text = (
        "The core classification system is developed using Term Frequency - Inverse Document Frequency (TF-IDF) feature extraction (unigrams and bigrams with sublinear term-frequency scaling) and a Multinomial Logistic Regression classifier with L2 regularization. The trained classifier computes class probabilities via the Softmax function, allowing the system to output both the predicted category and a percentage confidence score. In parallel, NLTK VADER calculates compound sentiment polarity scores (-1.0 to +1.0) with grievance deficiency adjustments, and a rule-based priority engine evaluates emergency/hazard keywords to assign High, Medium, or Low priority. The trained models are serialized using Joblib for real-time inference."
    )

    # Evaluation Metrics
    doc.paragraphs[24].text = "Evaluation Metrics"
    doc.paragraphs[25].text = (
        "The performance of the classification system was evaluated on a stratified 20% test split using standard machine learning evaluation metrics: Accuracy, Precision (weighted), Recall (weighted), and F1-Score (weighted). Multiple candidate algorithms were benchmarked on the dataset, including Multinomial Naive Bayes (Accuracy: 78.72%, F1-Score: 78.16%), Logistic Regression (Accuracy: 82.98%, F1-Score: 82.73%), Linear Support Vector Machine (Accuracy: 84.04%, F1-Score: 83.93%), and Random Forest (Accuracy: 75.53%, F1-Score: 75.61%). Logistic Regression was selected for the final application due to its strong generalization and native probability estimation."
    )

    # Results & Discussion
    doc.paragraphs[27].text = "Results & Discussion"
    doc.paragraphs[28].text = (
        "The developed Smart Student Complaint Analyzer successfully automates the grievance triage workflow with sub-second response times. When a student enters a complaint such as 'Need AC in class, room 214', the system normalizes the acronyms, accurately predicts the 'Classroom' category with high confidence (85%+), identifies negative grievance sentiment (-0.35), extracts relevant keywords ('AC', 'Air', 'Conditioning', 'Class'), and routes the complaint to the Administration department. The administrative portal provides live aggregated metrics, status tracking, and dynamic Chart.js visualizations for category, priority, and sentiment trends."
    )

    # Screenshots Section
    doc.paragraphs[31].text = "Screenshots"
    # Ensure paragraphs 32 to 39 remain blank space as requested
    for idx in range(32, 40):
        if idx < len(doc.paragraphs):
            doc.paragraphs[idx].text = ""

    # Conclusion
    doc.paragraphs[40].text = "Conclusion"
    doc.paragraphs[41].text = (
        "Smart Student Complaint Analyzer demonstrates a practical and effective application of Natural Language Processing and Machine Learning in educational administration. By automating complaint classification, sentiment analysis, priority assignment, and department routing, the system eliminates manual triage delays and improves campus responsiveness. The application provides a complete, scalable solution with a working web frontend, REST API, relational database integration, and analytics dashboard, serving as a solid foundation for future extensions such as multi-lingual support and mobile notifications."
    )

    # References
    doc.paragraphs[43].text = "References"
    doc.paragraphs[44].text = "Bird, S., Klein, E., & Loper, E., 'Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit', O'Reilly Media."
    doc.paragraphs[45].text = "Pedregosa, F., et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research, Vol. 12, pp. 2825-2830."
    doc.paragraphs[46].text = "Hutto, C., & Gilbert, E., 'VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text', Eighth International AAAI Conference on Weblogs and Social Media."
    doc.paragraphs[47].text = "Grinberg, M., 'Flask Web Development: Developing Web Applications with Python', O'Reilly Media."

    # Project Summary
    doc.paragraphs[49].text = "Project Summary"
    doc.paragraphs[50].text = (
        "Smart Student Complaint Analyzer combines natural language preprocessing, TF-IDF vectorization, machine learning classification, VADER sentiment analysis, and a responsive Flask web application into one cohesive campus grievance management system. The project highlights how foundational NLP techniques can be practically engineered to solve real-world institutional triage and tracking challenges."
    )

    doc.save('NLP_MINI_PROJECT_FINALL.docx')
    print("Updated NLP_MINI_PROJECT_FINALL.docx successfully in-place with original template formatting!")

if __name__ == '__main__':
    update_report_in_place()
