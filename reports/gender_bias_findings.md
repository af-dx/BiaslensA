# gender_bias_findings

* **Dataset:** `mediabiasgroup/mbib-base`
* **Split:** `gender_bias`
* **Size:** 17,939 rows
* **Columns:** `id`, `text`, `label`, `dataset_id`
* **Task:** Binary classification — `0` = no gender bias, `1` = gender bias present

---

## What We Found

* **Balanced Classes:** Classes are perfectly balanced — **8,969 / 8,970**.


* **Source:** The data comes from three underlying datasets:

| dataset_id | Rows | Positive Rate |
| :--- | :--- | :--- |
| **75** | 9,187 | 0.715 |
| **106** | 901 | 0.684 |
| **107** | 7,852 | 0.227 |

* **Data Cleanliness:**
  * Zero missing values.
  * Zero exact duplicate texts.
  * Zero non-ASCII characters and zero encoding artifacts.

* **Pre-processing:**
 No punctuation,
 no capitalisation,
 no emojis,
 no URLs.



* **Text Length:** Length does not separate the classes. Median is **16 words** for both labels. The model cannot cheat via text length.
* **ID Column Issue:** `id` is not a unique key. 2,664 IDs repeat, each with different text; they are local counters reused across the underlying datasets. **Use the row index instead.**
* **Validation Strategy:** No related examples need grouping. With no meaningful
  duplicates, a **plain stratified split** is sufficient — no `GroupKFold` required.
  Note that this addresses grouping only: because all three sources appear in every
  split, a stratified split measures **in-domain** performance.
---

## Decisions

* **Metric:** **Macro-F1**  Accuracy is valid in-domain given the 50/50 balance.
Supporting metrics: Precision, Recall, and Confusion Matrix

---

## Notes Presentation
Label distribution within each source plot

---

## Day 2 Summary — Gender Bias Detection

### Data

 Stratified 80/10/10 split: 14,313 / 1,790 / 1,790.


### Preventing leakage
No text appears in more than one split, and the texts carry no author identifiers.
.
### Key Findings — Baseline Experiment

- TF-IDF + Logistic Regression reached a validation **ROC-AUC of 0.9014**, with F1 of 0.8293 and accuracy of 0.8218.
- `DummyClassifier(most_frequent)` returned  meaningful floor is **F1 = 0.667** — the score of a constant predictor choosing the positive class.





### Results (validation set, primary metric: ROC-AUC)

| Model | ROC-AUC | F1 |
|---|---|---|
| LSTM (Embedding → LSTM → Dense) | 0.8777 | 0.8219 |
| **TF-IDF + Logistic Regression** | **0.8994** | 0.8286 |

### What we found

**All three models land in the same place.** Logistic Regression, LinearSVC and the
LSTM all score between 0.896 and 0.901 ROC-AUC. Changing the algorithm barely moves
the result, which tells us the limit is in the data, not the model choice.

**The LSTM didn't help.** It stopped improving after one epoch — 500K parameters
trained on 14K short sentences start memorising immediately.

**Some "errors" are actually wrong labels.** Among the sentences the model was most
confident about, several contain clearly biased content but are labelled unbiased in
the data. The model was right and got scored as wrong. This puts a ceiling on how
high any model can go here.
Some of what are counted as model errors are, in fact, errors in data labeling. This includes explicitly biased sentences that were labeled as unbiased in the dataset; the model classified them correctly, yet it was penalized for an error. This establishes a performance ceiling that no model can surpass.

**Overfitting check.** Train ROC-AUC 0.9418 vs validation 0.9014 — a gap of 0.040.
Reducing the feature count from 20,000 to 5,000 narrowed the gap from 0.057 while
*raising* validation ROC-AUC (0.8994 → 0.9014). Cross-validation (0.8922 ± 0.0023)
sits close to the validation score with minimal fold variance, confirming a stable
fit that generalises.

### What this means

To actually improve, we need better data, not a better model:
- positive and neutral examples that mention women, so the word stops predicting bias
- more varied sources
- a second pass over the labels
