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
