"""Complaint classification, priority calculation, department mapping, and full pipeline inference."""

import os
import joblib
import numpy as np
from pathlib import Path
from config import Config
from ml.preprocessing import preprocess_pipeline, extract_keywords
from ml.sentiment import analyze_sentiment

# Configurable Department Mapping
CATEGORY_DEPARTMENT_MAP = {
    "Academics": "Academic Department",
    "Examination": "Examination Cell",
    "IT & Wi-Fi": "IT Support",
    "Infrastructure": "Maintenance Department",
    "Classroom": "Administration",
    "Library": "Library Department",
    "Canteen": "Canteen Management",
    "Hostel": "Hostel Administration",
    "Transport": "Transport Department",
    "Administration": "Administrative Office",
    "Fees & Accounts": "Accounts Department",
    "Other": "General Administration"
}

# High-priority and critical urgency keyword lexicon
HIGH_PRIORITY_KEYWORDS = {
    'urgent', 'urgently', 'emergency', 'danger', 'dangerous', 'unsafe', 'fire',
    'accident', 'not working', 'blocked', 'deadline', 'exam', 'examination',
    'security', 'electricity', 'water', 'medical', 'hospital', 'spark', 'sparks',
    'shock', 'electric shock', 'fell', 'falling', 'collapse', 'collapsed',
    'hazard', 'stuck', 'trapped', 'shortage', 'poisoning', 'flooded', 'bleeding',
    'harassment', 'theft', 'threat', 'smoke', 'gas leak'
}

MEDIUM_PRIORITY_KEYWORDS = {
    'broken', 'slow', 'delay', 'delayed', 'damaged', 'noise', 'dirty', 'poor',
    'failed', 'missing', 'unresponsive', 'unhygienic', 'crowded', 'queue',
    'overcharged', 'glitch', 'error', 'odor', 'stink', 'rude'
}

# Cached model & vectorizer
_MODEL = None
_VECTORIZER = None


def load_ml_assets():
    """Load and cache the trained ML model and TF-IDF vectorizer."""
    global _MODEL, _VECTORIZER
    if _MODEL is None and Config.MODEL_PATH.exists():
        try:
            _MODEL = joblib.load(Config.MODEL_PATH)
        except Exception:
            _MODEL = None
            
    if _VECTORIZER is None and Config.VECTORIZER_PATH.exists():
        try:
            _VECTORIZER = joblib.load(Config.VECTORIZER_PATH)
        except Exception:
            _VECTORIZER = None
            
    return _MODEL, _VECTORIZER


def calculate_priority(text: str, sentiment_score: float, category: str) -> str:
    """
    Determine priority (High, Medium, Low) using rule-based NLP heuristics:
    - Urgent keyword matches
    - Strong negative sentiment (< -0.40)
    - Safety, Examination, and Critical Infrastructure categories
    """
    lower_text = text.lower()
    
    # Check urgent keyword presence
    urgent_hits = sum(1 for kw in HIGH_PRIORITY_KEYWORDS if kw in lower_text)
    medium_hits = sum(1 for kw in MEDIUM_PRIORITY_KEYWORDS if kw in lower_text)
    
    # Critical categories where issues easily cause major disruption
    critical_categories = {'Infrastructure', 'Hostel', 'Examination', 'IT & Wi-Fi'}
    
    # Priority Heuristic Rules:
    # 1. Any urgent keyword hit + negative sentiment or critical category -> High
    if urgent_hits > 0:
        return "High"
        
    # 2. Strong negative sentiment in critical categories -> High
    if sentiment_score <= -0.45 and category in critical_categories:
        return "High"
        
    # 3. Medium keyword hits or moderate negative sentiment -> Medium
    if medium_hits > 0 or sentiment_score < -0.10:
        return "Medium"
        
    # 4. General suggestions, neutral feedback, or positive remarks -> Low
    return "Low"


def predict_category(text: str) -> tuple:
    """
    Predict the complaint category and model confidence score.
    Returns: (category: str, confidence: float)
    """
    model, vectorizer = load_ml_assets()
    
    # Preprocess text
    processed_text = preprocess_pipeline(text)
    
    if not model or not vectorizer or not processed_text:
        # Fallback category if model is not yet trained
        return "Other", 50.0

    try:
        vec = vectorizer.transform([processed_text])
        
        # If probability estimation is supported (e.g. LogisticRegression)
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(vec)[0]
            max_idx = np.argmax(probabilities)
            category = model.classes_[max_idx]
            confidence = round(float(probabilities[max_idx]) * 100, 1)
        elif hasattr(model, "decision_function"):
            decision = model.decision_function(vec)[0]
            # Softmax on decision function for confidence
            exp_d = np.exp(decision - np.max(decision))
            probs = exp_d / np.sum(exp_d)
            max_idx = np.argmax(probs)
            category = model.classes_[max_idx]
            confidence = round(float(probs[max_idx]) * 100, 1)
        else:
            category = model.predict(vec)[0]
            confidence = 85.0

        # Confidence bounds safety
        confidence = max(40.0, min(99.9, confidence))
        return category, confidence
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Other", 50.0


def analyze_complaint(text: str) -> dict:
    """
    Full End-to-End NLP Pipeline:
    1. Preprocessing & Lemmatization
    2. Category Classification
    3. Model Confidence Score
    4. Sentiment Analysis & Polarity
    5. Priority Calculation
    6. Department Recommendation
    7. Keyword Extraction
    """
    if not text or not text.strip():
        return {
            "category": "Other",
            "confidence": 0.0,
            "sentiment": "Neutral",
            "sentiment_score": 0.0,
            "priority": "Low",
            "department": "General Administration",
            "keywords": []
        }

    # 1 & 2. Predict Category and Confidence
    category, confidence = predict_category(text)
    
    # 3. Sentiment Analysis
    sentiment_result = analyze_sentiment(text)
    sentiment_label = sentiment_result['sentiment']
    sentiment_score = sentiment_result['score']
    
    # 4. Priority Calculation
    priority = calculate_priority(text, sentiment_score, category)
    
    # 5. Department Mapping
    department = CATEGORY_DEPARTMENT_MAP.get(category, "Administrative Office")
    
    # 6. Keyword Extraction
    keywords = extract_keywords(text, top_n=5)
    
    return {
        "category": category,
        "confidence": confidence,
        "sentiment": sentiment_label,
        "sentiment_score": sentiment_score,
        "priority": priority,
        "department": department,
        "keywords": keywords
    }
