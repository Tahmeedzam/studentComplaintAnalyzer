"""Train Machine Learning model for Student Complaint Classification."""

import os
import sys
from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report

# Ensure project root is in python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import Config
from ml.preprocessing import preprocess_pipeline, ensure_nltk_resources


def train_complaint_classifier():
    """Execute training pipeline and save artifacts."""
    print("=" * 60)
    print(" SMART STUDENT COMPLAINT ANALYZER - MODEL TRAINING ")
    print("=" * 60)
    
    ensure_nltk_resources()

    dataset_path = Config.DATASET_PATH
    if not dataset_path.exists():
        print(f"[-] Error: Dataset not found at {dataset_path}")
        sys.exit(1)

    print(f"[*] Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"[*] Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"[*] Categories present ({df['category'].nunique()}): {list(df['category'].unique())}\n")

    # Preprocessing
    print("[*] Preprocessing text corpus (Cleaning, Stopwords removal, Lemmatization)...")
    df['clean_text'] = df['text'].apply(preprocess_pipeline)
    
    # Filter empty rows if any
    df = df[df['clean_text'].str.strip() != '']

    X = df['clean_text']
    y = df['category']

    # Train-test split (Stratified for balanced evaluation)
    print("[*] Splitting dataset into 80% Train and 20% Test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # TF-IDF Vectorization
    print("[*] Generating TF-IDF Features (unigrams + bigrams)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=4000,
        sublinear_tf=True,
        min_df=1
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"[*] Vocabulary size: {len(vectorizer.vocabulary_)} features")

    # Model Training: Multinomial Logistic Regression
    print("[*] Training Logistic Regression Classifier (LBFGS with L2 regularization)...")
    classifier = LogisticRegression(
        C=2.5,
        max_iter=1000,
        solver='lbfgs',
        random_state=42
    )
    classifier.fit(X_train_vec, y_train)

    # Evaluation
    print("\n" + "=" * 60)
    print(" MODEL PERFORMANCE EVALUATION (TEST SET) ")
    print("=" * 60)
    y_pred = classifier.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)

    print(f" Accuracy : {acc * 100:.2f}%")
    print(f" Precision: {precision * 100:.2f}%")
    print(f" Recall   : {recall * 100:.2f}%")
    print(f" F1 Score : {f1 * 100:.2f}%")
    print("-" * 60)
    print("Classification Report:\n")
    print(classification_report(y_test, y_pred, zero_division=0))
    print("=" * 60)

    # Save artifacts
    Config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Saving trained model to: {Config.MODEL_PATH}")
    joblib.dump(classifier, Config.MODEL_PATH)
    
    print(f"[*] Saving TF-IDF vectorizer to: {Config.VECTORIZER_PATH}")
    joblib.dump(vectorizer, Config.VECTORIZER_PATH)
    
    print("\n[+] Model training and export completed successfully!\n")


if __name__ == '__main__':
    train_complaint_classifier()
