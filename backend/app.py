from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import os

from src.schema import FEATURE_ORDER
from src.business_rules import check_business_rules
from src.labeling import decode_gpa_class
from src.feedback import generate_feedback

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend"),
    static_url_path=""
)
CORS(app)

# Absolute path to model (Render-safe)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "gpa_class_xgb_tuned.pkl")

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
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    missing_features = [f for f in INFERENCE_FEATURES if f not in data]
    if missing_features:
        return jsonify({
            "error": "Missing required features",
            "missing_features": missing_features
        }), 400

    try:
        user_df = pd.DataFrame(
            [[data[f] for f in INFERENCE_FEATURES]],
            columns=INFERENCE_FEATURES
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    features_dict = user_df.iloc[0].to_dict()

    rules_result = check_business_rules(features_dict)
    if not rules_result["allowed"]:
        return jsonify({
            "error": "Business rule violation",
            "reason": rules_result["reason"],
            "warnings": rules_result["warnings"]
        }), 400

    prediction_index = int(model.predict(user_df)[0])
    prediction_label = decode_gpa_class(prediction_index)

    feedback = generate_feedback(prediction_label, features_dict)

    return jsonify({
        "class_index": prediction_index,
        "prediction": prediction_label,
        "feedback": feedback
    }), 200


# REMOVE THIS BLOCK FOR RENDER DEPLOYMENT
if __name__ == "__main__":
    app.run(debug=True)
