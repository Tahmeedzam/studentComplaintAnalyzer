"""Sentiment analysis module using NLTK VADER with domain-aware grievance adjustments."""

import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from ml.preprocessing import ensure_nltk_resources

ensure_nltk_resources()

_VADER_ANALYZER = None


def get_vader_analyzer():
    """Lazy initialize and cache the VADER SentimentIntensityAnalyzer."""
    global _VADER_ANALYZER
    if _VADER_ANALYZER is None:
        try:
            _VADER_ANALYZER = SentimentIntensityAnalyzer()
        except Exception:
            _VADER_ANALYZER = None
    return _VADER_ANALYZER


# Deficiency & Grievance phrases that denote negative sentiment in student complaints
GRIEVANCE_DEFICIENCY_PATTERNS = [
    r"\bno\s+(ac|fan|fans|water|electricity|light|lights|wifi|internet|chair|chairs|bench|benches|audio|mic|projector)\b",
    r"\b(not\s+working|broken|damaged|leaking|leakage|dirty|unhygienic|smelly|stinking|stale|spoiled|mosquito|bed\s*bug)\b",
    r"\b(failed|crashing|crash|slow|late|delay|delayed|penalty|unfair|overcharged|shortage|disconnected|down)\b",
    r"\b(rude|unhelpful|harsh|terrible|worst|awful|poor|useless|pathetic|headache|pain)\b"
]


def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a complaint text using VADER + Domain Grievance Adjustments.
    
    Returns:
        dict: {
            'sentiment': 'Positive' | 'Neutral' | 'Negative',
            'score': float (-1.0 to 1.0),
            'pos': float,
            'neu': float,
            'neg': float
        }
    """
    if not text or not text.strip():
        return {
            'sentiment': 'Neutral',
            'score': 0.0,
            'pos': 0.0,
            'neu': 1.0,
            'neg': 0.0
        }

    lower_text = text.lower()
    analyzer = get_vader_analyzer()

    if analyzer:
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Check domain deficiency/grievance patterns
        deficiency_matches = sum(1 for p in GRIEVANCE_DEFICIENCY_PATTERNS if re.search(p, lower_text))
        
        # If student is reporting broken/missing facility (even if they wrote "please"), reflect negative sentiment
        if deficiency_matches > 0:
            if compound >= 0:
                compound = -0.35 * deficiency_matches
            else:
                compound = compound - (0.15 * deficiency_matches)
                
        compound = max(-1.0, min(1.0, round(compound, 2)))

        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        return {
            'sentiment': sentiment,
            'score': compound,
            'pos': round(scores['pos'], 2),
            'neu': round(scores['neu'], 2),
            'neg': round(max(scores['neg'], 0.4 if sentiment == 'Negative' else 0.0), 2)
        }
    
    # Fallback
    negative_words = {'broken', 'fail', 'terrible', 'worst', 'bad', 'poor', 'not working', 'damage', 'rude', 'late', 'faulty', 'hazard', 'no ac', 'no fan'}
    pos_count = 1 if 'thank' in lower_text or 'great' in lower_text else 0
    neg_count = sum(1 for w in negative_words if w in lower_text)
    
    score = -0.4 if neg_count > 0 else (0.4 if pos_count > 0 else 0.0)
    sentiment = 'Negative' if score < 0 else ('Positive' if score > 0 else 'Neutral')
    
    return {
        'sentiment': sentiment,
        'score': score,
        'pos': 0.0 if score <= 0 else 0.5,
        'neu': 0.5,
        'neg': 0.5 if score < 0 else 0.0
    }
