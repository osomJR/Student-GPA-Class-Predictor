import os
import joblib

from development.tune import tune_model

MODEL_PATH = "models/gpa_class_xgb_tuned.pkl"


def test_tune_creates_model_file():
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)

    tune_model()

    assert os.path.exists(MODEL_PATH)
