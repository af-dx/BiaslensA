# Text-Level Bias — EDA Findings

## Dataset Overview
- Total records: 9,018
- Label 0: 4,509 records
- Label 1: 4,509 records
- Class distribution: Balanced

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

## Notes for the Presentation
- Include the label distribution plot.
- Include the text length distribution plot.
- Include the text length by label plot.
- Discuss duplicate-text handling and potential label ambiguity.
- Check that identical texts do not cross dataset splits.
