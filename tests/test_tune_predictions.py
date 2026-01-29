import os
import joblib
import pandas as pd

from src.dataset import build_dataset


# Configuration
MODEL_PATH = "models/gpa_class_xgb_tuned.pkl"
RAW_DATA_PATH = "data/raw/student_data.csv"


def test_tuned_model_produces_predictions():
    """
    Ensure the tuned model can generate predictions
    on the validation dataset.
    """

    # 1. Ensure model exists
    assert os.path.exists(MODEL_PATH), "Tuned model file does not exist."

    # 2. Load model
    model = joblib.load(MODEL_PATH)

    # 3. Load raw data
    raw_df = pd.read_csv(RAW_DATA_PATH)

    # 4. Build dataset (60/20/20 split)
    _, X_val, _, _, y_val, _ = build_dataset(raw_df)

    # 5. Generate predictions
    predictions = model.predict(X_val)

    # 6. Assertions
    assert predictions is not None
    assert len(predictions) == len(y_val)
