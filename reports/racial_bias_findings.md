# Comprehensive Exploratory Data Analysis (EDA) Summary DAY1


This notebook covers the complete exploratory data analysis (EDA) for the racial bias dataset (`mbib_base_racial_bias.csv`), following Tracks A through D guidelines.

---

## 📌 Track A: Problem Formulation & Class Distribution
- **Task:** Binary text classification to detect racial/religious bias (`label = 0` vs `label = 1`).
- **Dataset Size:** 9,788 rows and 9 columns.
- **Class Balance:** Perfectly balanced dataset:
  - **Label 0:** 4,894 samples (50.0%)
  - **Label 1:** 4,894 samples (50.0%)
- **Data Sources (`dataset_id`):**
  - **Source 75:** 9,335 samples
  - **Source 110:** 453 samples

---

## 📌 Track B: Text Characteristics & Properties
- **Text Length Analysis:** Computed `word_count` and `char_count` for all texts.
- **URLs & Links:** 0 URLs found (100% clean of external links).
- **Contextual Keywords:** Frequently occurring terms include identity and group labels (e.g., "people", "black", "jews", "muslims"), requiring contextual analysis rather than simple keyword lookup.

---

## 📌 Track C: Data Quality & Privacy Assurance
- **Missing Values:** 0 missing or null values across all columns.
- **Exact Duplicates:** 0 duplicate text records.
- **Very Short Texts:** Identified 9 texts under 3 words (e.g., "Gay"). Retained all rows as per project guidelines prohibiting example deletion during exploration.
- **PII & Privacy Check:** Verified 100% clean of email addresses, phone numbers, and personal identification details.

---

## 📌 Track D: Problem & Domain Understanding
- **Real-world Meaning:** Evaluates subtle and explicit bias in social text content.
- **Primary Metrics:** **Accuracy** and **Macro F1-Score** (selected due to perfect 50/50 class balance).
- **Splitting Strategy:** Stratified train/test split on `label` to maintain balanced distribution.

---

## 📋 End-of-Day Checkpoint Summary
- **Problem:** Binary racial/religious bias detection.
- **Data Shape:** 9,788 rows × 9 columns.
- **Class Balance:** Perfectly balanced (4,894 per class).
- **Data Cleanliness:** 0 missing values, 0 duplicates, 0 PII leakages.
- **Modeling Readiness:** Clean, preprocessed, and ready for baseline modeling (TF-IDF + Logistic Regression / Random Forest).
---------------------------------------------------------------------------------------------------
# 📊 Phase Progress Report: Text Classification Pipeline (Racial Bias Detection)

## 1. Executive Summary
Successfully built, evaluated, and structured an end-to-end text classification pipeline for detecting racial bias using the `racial_bias` dataset. The workflow spans dataset preparation, data leakage prevention via strict 3-way stratified split, baseline modeling (Dummy & TF-IDF + Logistic Regression with 3-Fold Cross-Validation), deep learning implementation (Small LSTM with Early Stopping), and a unified model evaluation comparison.

---

## 2. Phase 1: Dataset Overview & Cleaning Pipeline

### Dataset Source & Characteristics
* **Source:** Hugging Face (`mediabiasgroup/mbib-base` -> `racial_bias` split)
* **Initial Size:** 9,788 rows × 4 columns
* **Target Variable:** Binary classification labels (`0` or `1`) indicating bias presence.

### Cleaning & Text Normalization Steps
1. **Text Normalization:**
   - Converted all text to lowercase.
   - Stripped extra whitespaces and normalized spacing patterns via regular expressions.
   - Handled missing values (`fillna("")`).
2. **Conflicting Label Removal:** Identified and removed ambiguous samples where identical normalized texts were assigned conflicting target labels.
3. **Deduplication:** Dropped exact duplicate rows based on normalized text, retaining the first occurrence.
4. **Validation Assertions:** Confirmed all labels strictly fall within binary bounds (`[0, 1]`) and normalized text keys are unique without missing values.

* **Cleaned Dataset Result:** Reduced from 9,788 to **9,784 rows** (4 rows removed due to duplicates/conflicts).
* **Class Balance:** Perfectly balanced distribution (**Class 0:** 4,893 samples | **Class 1:** 4,891 samples).

---

## 3. Phase 2: Advanced Three-Way Data Partitioning

To strictly prevent **Data Leakage**, a two-stage stratified partitioning strategy was executed using `StratifiedShuffleSplit` (`RANDOM_STATE = 42`):

1. **First Split (Train vs. Temporary Set):** Cleaned dataset divided into 80% Training set and 20% Temporary set.
2. **Second Split (Validation vs. Test Set):** 20% Temporary set split equally (50/50) into 10% Validation set and 10% Test set.

### Final Split Summary
* **Train Set:** 7,827 rows (80.0%) | Class Distribution: `{0: 0.50, 1: 0.50}`
* **Validation Set:** 978 rows (10.0%) | Class Distribution: `{0: 0.50, 1: 0.50}`
* **Test Set:** 979 rows (10.0%) | Class Distribution: `{0: 0.501, 1: 0.499}`
* **Data Leakage Verification:** Confirmed zero text overlap across sets (`Overlap = 0`).

---

## 4. Phase 3: Model Architecture & Implementation

### A. Dummy Classifier (Baseline)
* **Purpose:** Establishes a random baseline to verify pipeline integrity and fair data split.
* **Result:** `ROC-AUC: ~0.5112`, confirming a fair 50/50 starting baseline.

### B. TF-IDF + Logistic Regression Pipeline
* **Preprocessing:** `TfidfVectorizer(max_features=10000, stop_words='english')`.
* **Validation Strategy:** Evaluated using 3-Fold Stratified Cross-Validation on training data prior to final validation evaluation.
* **Performance:**
  * **Mean CV ROC-AUC:** `~0.7727`
  * **Validation ROC-AUC:** `0.7861`
  * **Accuracy:** `0.6984`
  * **F1-Score:** `0.6905`

### C. Deep Learning (Small LSTM)
* **Tokenization & Padding:**
  * Vocabulary fitted *strictly* on training text (`VOCAB_SIZE = 10000`, `MAX_LENGTH = 150`).
  * Post-padding applied to align input sequence lengths.
* **Architecture:**
  * `Embedding(input_dim=10000, output_dim=64, mask_zero=True)`
  * `LSTM(units=64)`
  * `Dense(units=1, activation='sigmoid')`
* **Training Configuration:**
  * Compiled with `Adam` optimizer and `binary_crossentropy` loss.
  * `EarlyStopping` callback (`monitor='val_loss'`, `patience=2`, `restore_best_weights=True`) executed to prevent overfitting.
* **Performance:**
  * **Validation ROC-AUC:** `0.7918`
  * **PR-AUC:** `0.7960`
  * **Accuracy:** `0.7320`
  * **F1-Score:** `0.7251`

---

## 5. Phase 4: Unified Model Comparison & Key Findings

### Unified Model Evaluation Table

| Model | ROC-AUC | PR-AUC | Accuracy | Precision | Recall | F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dummy Classifier** | 0.5112 | 0.5058 | 0.5112 | 0.5113 | 0.5092 | 0.5102 |
| **TF-IDF + Logistic Regression** | 0.7861 | 0.7815 | 0.6984 | 0.7091 | 0.6728 | 0.6905 |
| **Small LSTM** | 0.7918 | 0.7960 | 0.7320 | 0.7601 | 0.6933 | 0.7251 |

---

### Key Findings
1. **Pipeline Integrity:** The `Dummy Classifier` results (~0.51) confirm zero dataset bias and a reliable splitting methodology.
2. **Linear Baseline Strength:** `TF-IDF + Logistic Regression` provided a strong baseline (`ROC-AUC: 0.7861`), demonstrating that linear models offer fast and high-baseline performance.
3. **LSTM Superiority:** The `Small LSTM` achieved the highest performance across all key evaluation metrics (`ROC-AUC: 0.7918`, `Accuracy: 0.7320`, and `F1-Score: 0.7251`), proving its capability to capture contextual word order and sequential relationships effectively.
---------------------------------------------------------------------------------
### 📝 Day 3 Progress & Summary

#### 1. Overfitting & Model Comparison Framework
- **Unified Overfitting Code**: Combined the overfitting checks for all models (**LinearSVC**, **Small LSTM**, and **Logistic Regression**) into a single, clean code block to generate a comprehensive comparison table (Accuracy, F1-Score, and ROC-AUC).
- **Performance & Gap Analysis**:
  - **LinearSVC**: Demonstrated exceptional stability with almost zero overfitting ($\text{Gap} \approx -0.0048$).
  - **Logistic Regression**: Showed a very safe and acceptable minor gap ($\text{Gap} \approx 0.0920$).
  - **Small LSTM**: Exhibited the highest gap ($\text{Gap} \approx 0.1105$) due to neural network behavior, which was well-controlled using Dropout and Early Stopping.

#### 2. Error Analysis (Track D)
- **Error Classification**: Evaluated validation set predictions, resulting in 711 correct predictions, 154 False Negatives, and 113 False Positives.
- **Root Cause Documentation**:
  - **False Positives**: Safe texts incorrectly flagged as biased due to isolated keywords appearing within a neutral context.
  - **False Negatives**: Subtle or implicit bias missed by the model in certain samples.

#### 3. Model Persistence & Deployment Prep
- **Saving Artifacts**: Successfully saved all trained model pipelines and tokenizers to disk in `.joblib` and `.pkl` formats, ensuring they are fully ready for quick loading during the Demo Day.
