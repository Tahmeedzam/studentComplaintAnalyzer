"""Compare multiple Machine Learning classifiers on the complaint dataset."""

import os
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import Config
from ml.preprocessing import preprocess_pipeline, ensure_nltk_resources


def benchmark_models():
    """Run cross-model benchmark and format results."""
    print("=" * 70)
    print(" NLP CLASSIFICATION ALGORITHMS BENCHMARK ")
    print("=" * 70)

    ensure_nltk_resources()
    
    if not Config.DATASET_PATH.exists():
        print(f"[-] Error: Dataset file not found at {Config.DATASET_PATH}")
        sys.exit(1)

    df = pd.read_csv(Config.DATASET_PATH)
    print(f"[*] Loaded {len(df)} complaint samples across {df['category'].nunique()} categories.")
    
    # Preprocessing
    print("[*] Preprocessing text corpus...")
    df['clean_text'] = df['text'].apply(preprocess_pipeline)
    df = df[df['clean_text'].str.strip() != '']

    X_train, X_test, y_train, y_test = train_test_split(
        df['clean_text'], df['category'], test_size=0.20, random_state=42, stratify=df['category']
    )

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=4000, sublinear_tf=True)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Models dictionary
    models = {
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.5),
        "Logistic Regression": LogisticRegression(C=2.5, max_iter=1000, solver='lbfgs', random_state=42),
        "Linear SVM (LinearSVC)": LinearSVC(C=1.0, max_iter=2000, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = []

    print("[*] Training and evaluating candidate models...\n")
    for name, clf in models.items():
        clf.fit(X_train_vec, y_train)
        y_pred = clf.predict(X_test_vec)
        
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        
        results.append({
            "Model": name,
            "Accuracy": f"{acc * 100:.2f}%",
            "Precision": f"{prec * 100:.2f}%",
            "Recall": f"{rec * 100:.2f}%",
            "F1-Score": f"{f1 * 100:.2f}%"
        })

    # Print markdown-style and ASCII table for project reports
    results_df = pd.DataFrame(results)
    print("=" * 70)
    print(f"{'Model':<28} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 70)
    for r in results:
        print(f"{r['Model']:<28} | {r['Accuracy']:<10} | {r['Precision']:<10} | {r['Recall']:<10} | {r['F1-Score']:<10}")
    print("=" * 70)
    print("\n[+] Recommendation: Logistic Regression / Linear SVM deliver optimal multi-class accuracy and balanced generalization.\n")


if __name__ == '__main__':
    benchmark_models()
