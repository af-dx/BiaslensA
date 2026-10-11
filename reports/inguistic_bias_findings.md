# Day 1 — Key Findings & Conclusions

### 1. Dataset Overview
- The MBIB Linguistic Bias dataset contains **401,862 text samples** from **7 source datasets**.
- The overall class distribution is perfectly balanced: **50% Biased and 50% Unbiased**.
- Source 26 dominates the dataset, representing approximately **84.4%** of all samples.

### 2. Text Exploration
- Biased texts are longer on average (**61.9 vs. 34.1 words**), but median lengths are relatively similar (**29 vs. 25 words**).
- Text length distributions overlap considerably, making length alone an unreliable indicator of bias.
- The dataset contains different writing styles, ranging from formal news articles to informal online conversations.

### 3. Data Quality & Cleaning
- No missing or empty texts, exact duplicate texts, or detected replacement/null characters.
- **787 normalized duplicate groups** were identified, including **418 groups with conflicting labels**.
- Of these conflicts, **408 occur across Sources 3 and 26**, while **10 occur within Source 26**.
- After removing conflicting groups and consistent duplicates, the dataset was reduced to **400,657 samples**, retaining **99.7%** of the original data.
- **1,328 texts contain fewer than 5 words**, while **219 exceed 500 words** in the original dataset.

### 4. Domain Understanding
- Some labels are difficult to interpret without additional context or source-specific annotation guidelines.
- Bias prevalence varies significantly between sources (**14.17%–100%**).
- Source-specific writing styles and label distributions introduce potential shortcut-learning risks.

### 5. Final Decisions
- Preserve `df` as the original dataset and use `clean_df` as the preliminary modeling dataset.
- Use **ROC-AUC** as the primary evaluation metric, with PR-AUC, Precision, and Recall as supporting metrics.
- Prevent duplicate or related texts from crossing training and testing splits.
- Evaluate performance across different data sources to assess generalization.

### Conclusion

The dataset is balanced overall but heterogeneous across sources. Data cleaning resolved the identified normalized duplicate and conflicting-label groups with minimal data loss. The main remaining concerns are source-related shortcuts, label ambiguity, and potential leakage from related examples, which should guide the modeling and evaluation strategy.
