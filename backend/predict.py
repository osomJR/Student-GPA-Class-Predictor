"""
Prediction script for the Student GPA Class Predictor.

Responsibilities:
- Load trained model artifact
- Accept user input for required features
- Validate using business rules
- Predict GPA class label
"""
import random
import os
import joblib
import pandas as pd

from typing import Dict, List
from src.business_rules import check_business_rules
from src.schema import FEATURE_ORDER, TARGET_COLUMN
from src.labeling import decode_gpa_class
from src.feedback import generate_feedback

MODEL_PATH = "models/gpa_class_xgb_tuned.pkl"


# Features used for prediction (same as training)
PREDICT_FEATURES = [
    "average_attendance_per_course",
    "average_assignments_submission_per_course",
    "average_test_scores_per_course",
    "average_class_activities_and_engagements_per_course"
]


def _get_user_input() -> pd.DataFrame:
    """
    Collect input values for each feature from the user.
    """
    print("Enter the values for each feature below:")

    data = {}
    for feature in PREDICT_FEATURES:
        while True:
            value = input(f"{feature}: ").strip()
            if value == "":
                print("Input is required. Please enter a value.")
                continue
            try:
                data[feature] = float(value)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    return pd.DataFrame([data])


def predict():
    """
    Load model and predict class label for user input.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)

    user_df = _get_user_input()

    # Business rules validation
    features_dict = user_df.iloc[0].to_dict()
    rules_result = check_business_rules(features_dict)

    if not rules_result["allowed"]:
        print("Prediction blocked due to business rule violation.")
        print("Reason:", rules_result["reason"])
        return

    # Predict
    prediction_index = int(model.predict(user_df)[0])
    prediction_label = decode_gpa_class(prediction_index)

    # Generate personalized feedback
    feedback = generate_feedback(prediction_label, features_dict)

    print("predicted_GPA_class:", prediction_label)
    print("class_index:", prediction_index)
    print("feedback:", feedback)


if __name__ == "__main__":
    predict()
