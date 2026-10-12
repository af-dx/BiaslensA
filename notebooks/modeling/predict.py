import json, joblib
from pathlib import Path
from preprocessing import tokenize

ART = Path("artifacts")
_model  = joblib.load(ART / "logreg_pipeline.joblib")
_config = json.loads((ART / "config.json").read_text())
_LABELS = {0: "no bias", 1: "bias"}


def predict_bias(texts, threshold=None):
    threshold = threshold if threshold is not None else _config["threshold"]
    single = isinstance(texts, str)
    batch  = [texts] if single else list(texts)
    if not batch:
        return []
    probas = _model.predict_proba(batch)[:, 1]
    results = [
        {
            "text": t,
            "label": int(p >= threshold),
            "prediction": _LABELS[int(p >= threshold)],
            "confidence": round(float(p if p >= threshold else 1 - p), 4),
            "bias_probability": round(float(p), 4),
        }
        for t, p in zip(batch, probas)
    ]
    return results[0] if single else results
