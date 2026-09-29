"""Text preprocessing, acronym normalization, and keyword extraction utilities for the NLP pipeline."""

import os
import tempfile
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

_NLTK_DOWNLOADED = False


def ensure_nltk_resources():
    """Ensure required NLTK corpora and tokenizers are downloaded safely on demand."""
    global _NLTK_DOWNLOADED
    if _NLTK_DOWNLOADED:
        return
        
    nltk_data_dir = os.path.join(tempfile.gettempdir(), 'nltk_data')
    try:
        os.makedirs(nltk_data_dir, exist_ok=True)
    except Exception:
        pass
        
    if nltk_data_dir not in nltk.data.path:
        nltk.data.path.append(nltk_data_dir)

    resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4', 'vader_lexicon', 'punkt_tab']
    for res in resources:
        try:
            nltk.download(res, download_dir=nltk_data_dir, quiet=True)
        except Exception:
            pass
    _NLTK_DOWNLOADED = True


# Standard stop words with comprehensive static fallback (Zero network dependency)
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    'he', 'him', 'his', 'himself', 'she', 'her', 'it', 'its', 'they', 'them',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
    'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now'
}

try:
    STOP_WORDS = STOP_WORDS.union(set(stopwords.words('english')))
except Exception:
    pass

# Expanded conversational, domain, and filler stop words
DOMAIN_STOPWORDS = {
    'please', 'kindly', 'sir', 'madam', 'college', 'student', 'students',
    'issue', 'problem', 'need', 'needs', 'put', 'fast', 'there', 'theres',
    'want', 'wants', 'also', 'get', 'give', 'tell', 'make', 'take', 'come',
    'go', 'see', 'let', 'us', 'done', 'like', 'really', 'much', 'many',
    'look', 'even', 'still', 'know', 'say', 'said', 'one', 'two', 'due',
    'out', 'in', 'be'
}
COMBINED_STOPWORDS = STOP_WORDS.union(DOMAIN_STOPWORDS)

# Meaningful 2-letter campus acronyms that should NOT be filtered out
IMPORTANT_SHORT_TOKENS = {'ac', 'ip', 'os', 'ai', 'ml', 'id', 'ro', 'it', 'tv', 'ui'}

_LEMMATIZER = None


def get_lemmatizer():
    """Lazy initialize and cache the WordNetLemmatizer."""
    global _LEMMATIZER
    if _LEMMATIZER is None:
        try:
            _LEMMATIZER = WordNetLemmatizer()
        except Exception:
            _LEMMATIZER = None
    return _LEMMATIZER


def normalize_acronyms_and_slang(text: str) -> str:
    """Normalize campus slang, contractions, and acronyms (e.g., 'AC' -> 'ac air conditioning')."""
    if not text:
        return ""
    
    t = f" {text} "
    
    # Contractions
    t = re.sub(r"\bthere['’]?s\b", "there is", t, flags=re.IGNORECASE)
    t = re.sub(r"\bit['’]?s\b", "it is", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdon['’]?t\b", "do not", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcan['’]?t\b", "cannot", t, flags=re.IGNORECASE)
    t = re.sub(r"\bwon['’]?t\b", "will not", t, flags=re.IGNORECASE)
    t = re.sub(r"\bisn['’]?t\b", "is not", t, flags=re.IGNORECASE)
    t = re.sub(r"\bhasn['’]?t\b", "has not", t, flags=re.IGNORECASE)
    t = re.sub(r"\bhaven['’]?t\b", "have not", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdidn['’]?t\b", "did not", t, flags=re.IGNORECASE)
    
    # Common campus acronyms & abbreviations
    t = re.sub(r"\ba[/.]?c\b", "ac air conditioning", t, flags=re.IGNORECASE)
    t = re.sub(r"\bwi[- ]?fi\b", "wifi internet", t, flags=re.IGNORECASE)
    t = re.sub(r"\bprof(s)?\b", "professor", t, flags=re.IGNORECASE)
    t = re.sub(r"\blab(s)?\b", "laboratory practical", t, flags=re.IGNORECASE)
    t = re.sub(r"\bexam(s)?\b", "examination", t, flags=re.IGNORECASE)
    t = re.sub(r"\bwashroom(s)?|toilet(s)?|restroom(s)?\b", "restroom washroom", t, flags=re.IGNORECASE)
    t = re.sub(r"\bproj\b", "projector", t, flags=re.IGNORECASE)
    t = re.sub(r"\bfee(s)?\b", "fees tuition accounts", t, flags=re.IGNORECASE)
    
    return t.strip()


def clean_text(text: str) -> str:
    """Perform initial cleaning and normalization on raw text input."""
    if not text or not isinstance(text, str):
        return ""
    
    # 1. Normalize contractions & acronyms
    normalized = normalize_acronyms_and_slang(text)
    
    # 2. Lowercase conversion
    cleaned = normalized.lower().strip()
    
    # 3. Remove URLs & emails
    cleaned = re.sub(r'https?://\S+|www\.\S+', ' ', cleaned)
    cleaned = re.sub(r'\S+@\S+', ' ', cleaned)
    
    # 4. Remove unwanted punctuation & symbols (preserve alphanumeric and spaces)
    cleaned = re.sub(r'[^a-zA-Z\s-]', ' ', cleaned)
    
    # 5. Collapse multiple whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned


def tokenize_text(text: str) -> list:
    """Tokenize cleaned text into individual word tokens."""
    if not text:
        return []
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', text)
    return tokens


def remove_stopwords(tokens: list) -> list:
    """Filter out stop words while preserving crucial 2-letter campus acronyms."""
    filtered = []
    for t in tokens:
        lower_t = t.lower()
        if lower_t in IMPORTANT_SHORT_TOKENS:
            filtered.append(lower_t)
        elif lower_t not in COMBINED_STOPWORDS and len(lower_t) > 1:
            filtered.append(lower_t)
    return filtered


def lemmatize_tokens(tokens: list) -> list:
    """Lemmatize tokens to their base morphological forms."""
    lemmatizer = get_lemmatizer()
    if not lemmatizer:
        return tokens
    lemmatized = []
    for token in tokens:
        if token.lower() in IMPORTANT_SHORT_TOKENS:
            lemmatized.append(token.lower())
            continue
        try:
            lemmatized.append(lemmatizer.lemmatize(token))
        except Exception:
            lemmatized.append(token)
    return lemmatized


def preprocess_pipeline(text: str) -> str:
    """
    Execute full text preprocessing pipeline:
    Normalize -> Clean -> Tokenize -> Remove Stopwords -> Lemmatize -> Rejoin.
    """
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    filtered = remove_stopwords(tokens)
    lemmatized = lemmatize_tokens(filtered)
    return " ".join(lemmatized)


def extract_keywords(text: str, top_n: int = 5) -> list:
    """
    Extract key representative keywords from the raw complaint text.
    Preserves meaningful campus terms (like 'AC', 'Wi-Fi') and filters noise.
    """
    normalized = normalize_acronyms_and_slang(text)
    cleaned = clean_text(normalized)
    tokens = tokenize_text(cleaned)
    filtered = remove_stopwords(tokens)
    lemmatized = lemmatize_tokens(filtered)

    if not lemmatized:
        return []

    # Calculate token frequencies
    freq_dist = {}
    for word in lemmatized:
        w_lower = word.lower()
        if w_lower in COMBINED_STOPWORDS:
            continue
        if len(w_lower) >= 3 or w_lower in IMPORTANT_SHORT_TOKENS:
            freq_dist[w_lower] = freq_dist.get(w_lower, 0) + 1

    # Sort primarily by frequency, secondarily by length
    sorted_keywords = sorted(
        freq_dist.keys(),
        key=lambda w: (freq_dist[w], len(w)),
        reverse=True
    )
    
    formatted = []
    for w in sorted_keywords[:top_n]:
        if w in {'ac', 'ip', 'os', 'ai', 'ml', 'id', 'ro', 'it', 'tv', 'ui', 'wifi'}:
            formatted.append(w.upper() if w != 'wifi' else 'Wi-Fi')
        else:
            formatted.append(w.capitalize())
            
    return formatted
