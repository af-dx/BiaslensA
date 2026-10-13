"""BiasLens unified inference for four approved Logistic Regression pipelines.

The saved sklearn Pipelines contain their own fitted text preprocessing.
This module ONLY loads them and runs predictions. No fitting or retraining.

Public functions:
    analyze_text(text, threshold=0.5) -> dict
    predict_batch(texts, threshold=0.5) -> list[dict]
    api_predict(payload) -> dict
"""

from __future__ import annotations

import importlib
import json
import sys
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# src/predict.py lives one directory below the BiasLens project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

# Ensure src.preprocessing is importable even when this file is run directly.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Filenames match the working Final Predictions notebook.
MODEL_FILES = {
    "linguistic_bias": "linguistic_bias_lr_word_char.joblib",
    "gender_bias": "gender_bias_lr.joblib",
    "racial_bias": "racial_bias_lr.joblib",
    "context_bias": "text_level_bias_logistic_regression_c1.joblib",
}

BIAS_NAMES = {
    "linguistic_bias": "Linguistic Bias",
    "gender_bias": "Gender Bias",
    "racial_bias": "Racial Bias",
    "context_bias": "Context Bias",
}


@lru_cache(maxsize=1)
def _load_models():
    """Load each trusted saved model once per Python process.

    Restart the Python/Streamlit process after replacing model artifacts.
    """
    # The saved Gender pipeline references src.preprocessing.tokenize.
    try:
        importlib.import_module("src.preprocessing")
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Gender model requires src/preprocessing.py exposing the original "
            "tokenize() function. Keep src/genderpreprocessing.py unchanged."
        ) from exc

    missing = [
        filename for filename in MODEL_FILES.values()
        if not (MODELS_DIR / filename).is_file()
    ]
    if missing:
        raise FileNotFoundError(
            "Missing approved model file(s) inside models/: " + ", ".join(missing)
        )

    models = {}
    positive_indices = {}

    for bias, filename in MODEL_FILES.items():
        model = joblib.load(MODELS_DIR / filename)  # Trusted team artifacts only.

        if not isinstance(model, Pipeline):
            raise TypeError(f"{bias}: expected a saved, fitted sklearn Pipeline.")
        if not isinstance(model.steps[-1][1], LogisticRegression):
            raise TypeError(f"{bias}: final estimator must be LogisticRegression.")
        if not hasattr(model, "predict_proba"):
            raise TypeError(f"{bias}: pipeline has no predict_proba().")

        classes = np.asarray(model.classes_)
        if set(classes.tolist()) != {0, 1}:
            raise ValueError(f"{bias}: expected labels 0 and 1, got {classes}.")

        models[bias] = model
        positive_indices[bias] = int(np.flatnonzero(classes == 1)[0])

    return models, positive_indices


def _check_text(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non-empty string.")
    return text  # Keep the original text; preprocessing is inside each pipeline.


def _check_threshold(threshold):
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
        raise ValueError("Threshold must be numeric.")
    if not np.isfinite(threshold) or not 0 < threshold < 1:
        raise ValueError("Threshold must be between 0 and 1 (exclusive).")
    return float(threshold)


def predict_batch(texts, threshold=0.5):
    """Return four independent bias predictions for every input text."""
    if not isinstance(texts, (list, tuple)) or not texts:
        raise ValueError("Provide a non-empty list or tuple of text strings.")
    texts = [_check_text(text) for text in texts]
    threshold = _check_threshold(threshold)

    models, positive_indices = _load_models()
    scores_by_bias = {}

    for bias, model in models.items():
        probabilities = np.asarray(model.predict_proba(texts), dtype=float)
        if probabilities.shape != (len(texts), 2):
            raise RuntimeError(f"{bias}: unexpected probability array shape.")

        scores = probabilities[:, positive_indices[bias]]
        if not np.isfinite(scores).all():
            raise RuntimeError(f"{bias}: model returned a non-finite score.")
        if ((scores < 0) | (scores > 1)).any():
            raise RuntimeError(f"{bias}: model score must be between 0 and 1.")
        scores_by_bias[bias] = scores

    output = []
    for i, text in enumerate(texts):
        predictions = {}
        for bias in MODEL_FILES:
            probability = float(scores_by_bias[bias][i])
            label = int(probability >= threshold)  # Threshold BEFORE rounding.
            predictions[bias] = {
                "probability": round(probability, 4),
                "predicted_label": label,
                "prediction": "Biased" if label else "Unbiased",
            }

        output.append({
            "text": text,
            "threshold": threshold,
            "predictions": predictions,
            "detected_biases": [
                bias for bias, item in predictions.items()
                if item["predicted_label"] == 1
            ],
        })

    return output


def analyze_text(text, threshold=0.5):
    """Analyze one text (the main entry point for Streamlit)."""
    return predict_batch([text], threshold=threshold)[0]


def api_predict(payload):
    """JSON-ready wrapper, not an HTTP server or external API call."""
    if not isinstance(payload, dict) or "text" not in payload:
        raise ValueError("Payload must be a dictionary containing 'text'.")
    return analyze_text(payload["text"], payload.get("threshold", 0.5))


if __name__ == "__main__":
    example = "The committee announced its decision yesterday."
    print(json.dumps(analyze_text(example), indent=2, ensure_ascii=False))
