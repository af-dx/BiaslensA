<div align="center">

# BiasLens

### NLP-Powered Text Bias Detection & Analysis

**See Beyond the Words.**

Explore potential bias in written English through four independent NLP classifiers, brought together in an interactive web application.

[**Try the Live App**](https://biaslens-wxushdmevfi8z3jzd3uknv.streamlit.app/) · [**Explore the Dataset**](https://huggingface.co/datasets/mediabiasgroup/mbib-base)

*Saudi Digital Academy × Le Wagon — Data Science & AI Bootcamp | October 2026*

</div>

---

## Overview

Bias can be expressed through wording, framing, and stereotypes, and may be difficult to recognize consistently. **BiasLens** is an exploratory text-screening tool that brings four task-specific machine learning models into one accessible interface.

The project investigates a central question:

> **Can the same machine learning approach detect different forms of bias in written media?**

Our results suggest that a shared approach can learn bias-related patterns across different tasks, with performance varying by task and dataset.

## Four Bias Categories

| Category | What the model screens for |
| --- | --- |
| **Linguistic Bias** | Potentially biased wording and framing |
| **Gender Bias** | Gender-related stereotypes and assumptions |
| **Racial Bias** | Race- or ethnicity-related stereotypes |
| **Text-Level / Context Bias** | Potential bias patterns at the text level |

Each category has its **own binary classifier**. A passage may be flagged in multiple categories, or in none.

## How It Works

1. **Enter text** — Paste an English sentence or short passage, or choose a built-in example.
2. **Analyze** — BiasLens processes the text using four separately trained classification pipelines.
3. **Explore results** — Review category-level predictions, positive-class model scores, and an interactive bias profile.

The interface also includes **Model Insights** and **About** pages.

## Dataset and Approach

We use four tasks from [MBIB-base (Media Bias Identification Benchmark)](https://huggingface.co/datasets/mediabiasgroup/mbib-base).

| Task | Original records |
| --- | ---: |
| Linguistic Bias | 401,862 |
| Gender Bias | 17,940 |
| Racial Bias | 9,788 |
| Text-Level / Context Bias | 9,018 |

The deployed models use **TF-IDF features and Logistic Regression**, with task-specific preprocessing and feature configurations. Development also explored alternatives such as **LinearSVC**, **LSTM**, and a **limited DistilBERT experiment**. Model selection emphasized ROC-AUC alongside precision, recall, F1-score, and error analysis.

## Final Test Results

| Task | ROC-AUC | Precision | Recall | F1-score |
| --- | ---: | ---: | ---: | ---: |
| Linguistic Bias | 0.6959 | 0.6647 | 0.5699 | 0.6137 |
| Gender Bias | 0.8695 | 0.7540 | 0.8468 | 0.7977 |
| Racial Bias | 0.7724 | 0.7000 | 0.7469 | 0.7227 |
| Text-Level / Context Bias | 0.7679 | 0.6993 | 0.7086 | 0.7039 |

*Each classifier was evaluated on its own held-out test set. Results across different tasks are not directly comparable as a head-to-head model ranking.*

## Try BiasLens

**Live application:** https://biaslens-wxushdmevfi8z3jzd3uknv.streamlit.app/

### Run Locally

```bash
# Clone the repository
git clone https://github.com/altaleb-sarah/BiasLens.git
cd BiasLens

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS / Linux

# Install dependencies and start the app
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

## Limitations and Future Directions

BiasLens is a **decision-support and exploratory screening tool**, not a definitive judge of biased language. False positives and false negatives remain possible, and the current models may struggle with subtle meaning, counter-speech, and unfamiliar sources. The application currently focuses on **English text**. Model scores are **not validated bias-severity measurements** or calibrated probabilities across tasks.

Future directions include improved contextual modeling, broader and more representative data, clearer prediction explanations, external evaluation, and potential multilingual support, including Arabic.

## Project Team

| Member | Role |
| --- | --- |
| **Sarah Altaleb** | Project Creator & Team Lead |
| Hadeel Alghashmari | Team Contributor |
| Afnan Alhasni | Team Contributor |
| Nouf Alsufyani | Team Contributor |

## Technology

Python · scikit-learn · NLP · TF-IDF · Logistic Regression · Streamlit · Plotly

## References

- [MBIB-base on Hugging Face](https://huggingface.co/datasets/mediabiasgroup/mbib-base)
- Wessel et al. (2023), *Introducing MBIB — the first Media Bias Identification Benchmark Task and Dataset Collection*. [DOI](https://doi.org/10.1145/3539618.3591882)

---

<div align="center"><strong>BiasLens — See Beyond the Words.</strong></div>
