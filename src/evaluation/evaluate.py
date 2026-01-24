"""
Model evaluation pipeline for the Student GPA Class Predictor.

Responsibilities:
- Load raw student data
- Build train/validation/test datasets via dataset.py
- Load trained model artifact
- Evaluate model on the TEST set (20%)
- Print evaluation metrics
"""

import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from src.dataset import build_dataset


# ----------------------------
# Configuration
# ----------------------------
RAW_DATA_PATH = "data/raw/student_data.csv"
MODEL_PATH = "models/gpa_class_xgb_tuned.pkl"  # or gpa_class_model.pkl
RANDOM_STATE = 42


def evaluate_model(model_path: str = MODEL_PATH) -> None:
    """
    Evaluate a saved model on the TEST set.
    """

    # 1. Load raw data
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw data not found at: {RAW_DATA_PATH}")

    raw_df = pd.read_csv(RAW_DATA_PATH)

    # 2. Build dataset
    X_train, X_val, X_test, y_train, y_val, y_test = build_dataset(raw_df)

    # 3. Load model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}")

    model = joblib.load(model_path)

    # 4. Predict on TEST set
    y_pred = model.predict(X_test)

    # 5. Print evaluation metrics
    print("\nTEST METRICS")
    print("-----------")
    print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision : {precision_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"Recall    : {recall_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"F1 Score  : {f1_score(y_test, y_pred, average='weighted'):.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    evaluate_model()
