# Natural Language Processing & Machine Learning Pipeline

This document explains the technical architecture, mathematical foundations, and implementation details of the NLP pipeline used in the **Smart Student Complaint Analyzer**.

---

## 1. Pipeline Overview

```
User Complaint Text
        │
        ▼
[1] Text Cleaning & Normalization (Lowercasing, Regex URL/Special Char Removal)
        │
        ▼
[2] Tokenization (NLTK word_tokenize)
        │
        ▼
[3] Stop Word Removal (NLTK English + Custom Academic Domain Lexicon)
        │
        ▼
[4] Morphological Lemmatization (WordNet Lemmatizer)
        │
        ▼
[5] TF-IDF Vectorization (Unigrams + Bigrams, Sublinear Term Frequency)
        │
        ▼
[6] Supervised Classification (Multinomial Logistic Regression with Softmax Proba)
        │
        ├─────────────────────────────┬─────────────────────────────┐
        ▼                             ▼                             ▼
Category Prediction           Sentiment Analysis            Priority Calculation
  & Confidence (%)             (NLTK VADER Compound)        (Urgency Lexicon + Rules)
        │                             │                             │
        └─────────────────────────────┴─────────────────────────────┘
                                      │
                                      ▼
                        Department Routing & Storage
```

---

## 2. Step-by-Step Methodology

### Step 1: Text Cleaning & Normalization
Raw complaints often contain noise such as non-standard characters, email addresses, URLs, and arbitrary casing.
- **Lowercasing**: Converts all characters to lowercase to prevent vocabulary fragmentation (e.g., `WiFi` vs `wifi`).
- **Regex Cleaning**: Strips email patterns (`\S+@\S+`), URLs (`https?://\S+`), and special symbols.

### Step 2 & 3: Tokenization & Stop Words Removal
- **Tokenization**: Segments the clean string into discrete word tokens.
- **Stop Words**: Filters out high-frequency grammatical functional words (`the`, `is`, `at`, `which`) and academic fillers (`please`, `sir`, `kindly`) that carry zero discriminatory signals for classification.

### Step 4: WordNet Lemmatization
Unlike crude stemming (which merely chops word endings), **Lemmatization** uses a morphological dictionary (WordNet) to reduce words to their true root dictionary forms:
- `disconnecting` $\rightarrow$ `disconnect`
- `leaking` $\rightarrow$ `leak`
- `computers` $\rightarrow$ `computer`

### Step 5: TF-IDF Feature Representation
The processed text is transformed into a numerical vector using **Term Frequency - Inverse Document Frequency (TF-IDF)**:

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

Where:
- $\text{TF}(t, d) = 1 + \ln(\text{count}(t, d))$ (Sublinear term frequency scaling)
- $\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$
- **N-Grams**: Unigrams $(1)$ and Bigrams $(2)$ capture collocations like `not working`, `water leak`, `late fee`.

### Step 6: Multi-Class Logistic Regression Classification
The classification model computes class probabilities using the **Softmax** function:

$$P(Y = c \mid \mathbf{x}) = \frac{e^{\mathbf{w}_c^T \mathbf{x} + b_c}}{\sum_{j=1}^{K} e^{\mathbf{w}_j^T \mathbf{x} + b_j}}$$

The category with highest probability is predicted, and the probability value is formatted as the **Confidence Score (%)**.

---

## 3. Sentiment Analysis (VADER)
**VADER (Valence Aware Dictionary and sEntiment Reasoner)** is a rule-based sentiment analysis engine tuned for conversational sentiment.
It computes a normalized **Compound Polarity Score** between $-1.0$ (Extremely Negative) and $+1.0$ (Extremely Positive):

- **Positive**: $\text{Compound} \ge +0.05$
- **Neutral**: $-0.05 < \text{Compound} < +0.05$
- **Negative**: $\text{Compound} \le -0.05$

---

## 4. Smart Priority Calculation Engine
Priority is calculated dynamically using a hybrid rule engine:
1. **High Priority**:
   - Presence of safety, emergency, or critical hazard keywords (`urgent`, `fire`, `sparks`, `danger`, `hospital`, `collapsed`, `flooded`, `food poisoning`, `deadline`).
   - Severe negative sentiment ($\text{score} \le -0.45$) occurring in critical infrastructure or examination categories.
2. **Medium Priority**:
   - Presence of standard operational defect keywords (`broken`, `delay`, `damaged`, `odor`, `slow`) or negative sentiment ($\text{score} < -0.10$).
3. **Low Priority**:
   - Neutral inquiries, positive feedback, or general suggestions.

---

## 5. Model Evaluation Metrics
During training, the system computes and logs:
- **Accuracy**: $\frac{TP + TN}{Total}$
- **Precision**: $\frac{TP}{TP + FP}$
- **Recall**: $\frac{TP}{TP + FN}$
- **F1 Score**: $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$
