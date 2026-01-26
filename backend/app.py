from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import os

from src.schema import FEATURE_ORDER
from src.business_rules import check_business_rules

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

MODEL_PATH = "models/gpa_class_xgb_tuned.pkl"

model = joblib.load(MODEL_PATH)

# Align inference features with dataset.py
INFERENCE_FEATURES = [
    f for f in FEATURE_ORDER if f != "previous_semester_gpa_scaled"
]

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expected JSON payload:
    {
        "average_attendance_per_course": 78,
        "average_assignments_submission_per_course": 80,
        "average_test_scores_per_course": 85,
        "average_class_activities_and_engagements_per_course": 90
    }
    """

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    print("Received data:", data)

    # Ensure all required inference features are present
    missing_features = [f for f in INFERENCE_FEATURES if f not in data]
    if missing_features:
        return jsonify({
            "error": "Missing required features",
            "missing_features": missing_features
        }), 400

    # Convert to DataFrame (ONLY 4 FEATURES, SAME ORDER AS TRAINING)
    try:
        user_df = pd.DataFrame(
            [[data[f] for f in INFERENCE_FEATURES]],
            columns=INFERENCE_FEATURES
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    # Business rules validation (still applied)
    rules_result = check_business_rules(user_df.iloc[0].to_dict())
    if not rules_result["allowed"]:
        return jsonify({
            "error": "Business rule violation",
            "reasons": rules_result["reasons"]
        }), 400

    # Predict
    prediction = model.predict(user_df)[0]

    return jsonify({
        "prediction": int(prediction)
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
