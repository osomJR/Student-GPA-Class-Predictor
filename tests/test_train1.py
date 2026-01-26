import os
import joblib

from development.train import train_model


def test_train_model_creates_model_file(tmp_path, monkeypatch):
    """
    Smoke test for training pipeline.
    Ensures training runs and model artifact is created.
    """

    # Redirect model output to temp directory
    model_path = tmp_path / "model.pkl"

    monkeypatch.setattr(
        "development.train.MODEL_OUTPUT_PATH",
        str(model_path)
    )

    # Run training
    train_model()

    # Assert model file was created
    assert model_path.exists()

    # Assert model can be loaded
    model = joblib.load(model_path)
    assert model is not None
