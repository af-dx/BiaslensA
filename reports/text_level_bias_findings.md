# Text-Level Bias — EDA Findings

## Dataset Overview
- Total records: 9,018
- Label 0: 4,509 records
- Label 1: 4,509 records
- Class distribution: Balanced

## Dataset Sources
* Number of source datasets: 2
* Dataset ID 76: 8,597 records (95.3%)
* Dataset ID 19: 421 records (4.7%)

The dataset is dominated by source 76, while source 19 represents a much smaller portion of the data.

## Label Distribution by Source
* Source 19: 88.1% Unbiased and 11.9% Biased.
* Source 76: 48.1% Unbiased and 51.9% Biased.

Label distribution varies substantially between the two sources. This may affect model performance, so evaluation by source may help identify differences in model behavior.

## Data Split Validation
* Training set: 7,214 records (80%).
* Validation set: 902 records (10%).
* Test set: 902 records (10%).
* Random seed: 42.
* Group-aware splitting was used to keep identical normalized texts in the same split.
* No shared normalized text groups were found across train, validation, and test sets.
* Label proportions were reasonably similar across the three splits.

The split was checked for text overlap to reduce the risk of data leakage. Author-level overlap could not be verified because author identifiers were not available in the dataset.

## Data Quality
- Missing values: 0
- Empty texts: 0
- Exact duplicate rows: 0
- Repeated text records: 2
- Texts with conflicting labels: 1

## Example of a Label Conflict
The text "no" appears with both label 0 and label 1.
This may indicate annotation ambiguity and should be reviewed.

## Evaluation Plan
- Data split: 80% train, 10% validation, 10% test
- Main metric: F1-score
- Supporting metrics: Precision, Recall, and Confusion Matrix

### Final Model Selection

Based on the validation results, Tuned Logistic Regression with TF-IDF and **C = 1** was selected as the final Logistic Regression configuration. It achieved a ROC-AUC of **0.7902** and a PR-AUC of **0.7912**, slightly outperforming LSTM v3 on both ranking metrics.

Although LSTM v3 achieved higher accuracy and F1-score, Logistic Regression was retained as the selected configuration due to its stronger ROC-AUC and PR-AUC performance. The final model choice will be further assessed using the held-out test set.
