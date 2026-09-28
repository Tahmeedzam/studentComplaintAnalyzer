"""Unit tests for NLP preprocessing, sentiment analysis, priority heuristics, and classification."""

import pytest
from ml.preprocessing import clean_text, tokenize_text, remove_stopwords, lemmatize_tokens, preprocess_pipeline, extract_keywords
from ml.sentiment import analyze_sentiment
from ml.prediction import calculate_priority, analyze_complaint


def test_clean_text():
    raw = "The Wi-Fi in http://college.edu Library is NOT working!! 123"
    cleaned = clean_text(raw)
    assert "http" not in cleaned
    assert "123" not in cleaned
    assert cleaned.islower()
    assert "library" in cleaned


def test_preprocessing_pipeline():
    text = "The professors are canceling classes without notices"
    processed = preprocess_pipeline(text)
    assert isinstance(processed, str)
    assert len(processed) > 0
    # Stopword 'are' should be removed
    assert "are" not in processed.split()


def test_sentiment_analysis():
    # Negative test
    neg_res = analyze_sentiment("The food served in the mess was terrible and unhygienic.")
    assert neg_res['sentiment'] == 'Negative'
    assert neg_res['score'] < 0

    # Positive test
    pos_res = analyze_sentiment("The new library facilities are excellent and helpful.")
    assert pos_res['sentiment'] == 'Positive'
    assert pos_res['score'] > 0

    # Neutral test
    neu_res = analyze_sentiment("Library is on the second floor.")
    assert neu_res['sentiment'] in {'Neutral', 'Positive', 'Negative'}


def test_priority_calculation():
    # Emergency keyword -> High
    high_prio = calculate_priority("Emergency fire hazard in chemistry lab!", -0.7, "Infrastructure")
    assert high_prio == "High"

    # Urgent electricity spark -> High
    spark_prio = calculate_priority("Electrical wires are sparking near room 102", -0.5, "Classroom")
    assert spark_prio == "High"

    # Mild/Neutral issue -> Low
    low_prio = calculate_priority("General suggestion to add a suggestion box in corridor", 0.1, "Other")
    assert low_prio == "Low"


def test_extract_keywords():
    text = "The library air conditioning system has broken down during exams"
    keywords = extract_keywords(text, top_n=3)
    assert isinstance(keywords, list)
    assert len(keywords) > 0
    # Check that keywords are non-empty strings
    for kw in keywords:
        assert len(kw) >= 2


def test_full_nlp_analysis():
    text = "Campus Wi-Fi in the hostel is extremely slow and disconnects frequently."
    result = analyze_complaint(text)
    
    assert "category" in result
    assert "confidence" in result
    assert "sentiment" in result
    assert "sentiment_score" in result
    assert "priority" in result
    assert "department" in result
    assert "keywords" in result
    assert isinstance(result['keywords'], list)
    assert result['confidence'] > 0
