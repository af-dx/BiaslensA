# BiasLens notebooks

كل عضوة تعمل في notebook مستقلة. القوالب تحتوي عناوين وتعليمات وخلايا كود فارغة، دون حلول أو نتائج جاهزة.

| Notebook | Task |
| --- | --- |
| `01_linguistic_bias.ipynb` | Linguistic bias |
| `02_gender_bias.ipynb` | Gender bias |
| `03_racial_bias.ipynb` | Racial bias |
| `04_context_bias.ipynb` | Context bias — confirm the official fourth task name |

## Before training

Confirm the official dataset/config/revision and label mapping. Compare the modeling plan with the actual Le Wagon guide; no course guide was available when these templates were prepared.

Proposed settings, pending team agreement: seed 42; 80/10/10 train/validation/test; Macro F1; stratified 5-fold CV on training only, with group-aware splitting/CV when required. Fit learned preprocessing inside each training fold. Keep test untouched until model selection is complete.

## Open in VS Code

Clone the repository, open its folder, install the Python and Jupyter extensions, then select your project environment as the notebook kernel. Install the starter dependencies with `python -m pip install -r requirements.txt`. This file does not install TensorFlow/Keras; configure those separately if required.

Work in your own notebook and a short-lived branch. Commit and push regularly, then open a pull request. Do not edit another member's notebook or commit raw data, secrets, or trained model binaries.

## Model handoff

Each task exports its own model and preprocessing artifact, label mapping, dependency versions, validation/test metrics, and a load-and-predict example. One application calls all four independent predictors on the same input text. Agree on artifact storage and loading paths before integration.
