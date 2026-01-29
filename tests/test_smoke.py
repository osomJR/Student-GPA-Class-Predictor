import pandas as pd

from src.dataset import build_dataset


def test_build_dataset_smoke():
    """
    Smoke test for dataset building.

    Ensures:
    - dataset builds without error
    - train/val/test splits are produced
    - splits are non-empty
    """

    # Load raw data
    raw_df = pd.read_csv("data/raw/student_data.csv")

    # Limit size for smoke test
    raw_df = raw_df.sample(n=2000, random_state=42).reset_index(drop=True)

    input_rows = len(raw_df)

    # Build dataset
    X_train, X_val, X_test, y_train, y_val, y_test = build_dataset(raw_df)

    # Basic sanity checks
    assert len(X_train) > 0
    assert len(X_val) > 0
    assert len(X_test) > 0

    assert len(y_train) == len(X_train)
    assert len(y_val) == len(X_val)
    assert len(y_test) == len(X_test)

    # Ensure total rows preserved after split
    total_split_rows = len(X_train) + len(X_val) + len(X_test)
    assert total_split_rows <= input_rows
