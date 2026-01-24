def test_model_produces_predictions(tmp_path, monkeypatch):
    from src.models.train import train_model
    import joblib
    import pandas as pd

    model_path = tmp_path / "model.pkl"
    monkeypatch.setattr(
        "src.models.train.MODEL_OUTPUT_PATH",
        str(model_path)
    )

    train_model()
    model = joblib.load(model_path)

    # Minimal dummy input (must match feature columns)
    X_dummy = pd.DataFrame([{
        "average_attendance_per_course": 80,
        "average_assignments_submission_per_course": 75,
        "average_test_scores_per_course": 70,
        "average_class_activities_and_engagements_per_course": 85,
    }])

    prediction = model.predict(X_dummy)
    assert prediction.shape == (1,)
