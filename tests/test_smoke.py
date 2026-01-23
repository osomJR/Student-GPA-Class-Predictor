import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.dataset import build_dataset


def test_build_dataset_smoke():
    # Load raw data
    raw_df = pd.read_csv("data/raw/student_data.csv")

    # Limit size for smoke test
    raw_df = raw_df.sample(n=2000, random_state=42).reset_index(drop=True)

    input_rows = len(raw_df)

    # Build dataset
    X_train, X_val, y_train, y_val = build_dataset(raw_df)

    # --------------------
    # Dataset visibility
    # --------------------
    total_used = len(X_train) + len(X_val)

    print("\nDATASET PIPELINE SUMMARY")
    print(f"Input rows              : {input_rows}")
    print(f"Rows after filtering    : {total_used}")
    print(f"Dropped rows            : {input_rows - total_used}")
    print(f"Train rows              : {len(X_train)}")
    print(f"Validation rows         : {len(X_val)}")
    print(f"Train ratio             : {len(X_train) / total_used:.2f}")
    print(f"Validation ratio        : {len(X_val) / total_used:.2f}")

    # --------------------
    # Train simple model
    # --------------------
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(max_iter=5000, random_state=42))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    # --------------------
    # Metrics visibility
    # --------------------
    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_val, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_val, y_pred, average="weighted", zero_division=0)

    print("\nMODEL METRICS (Smoke Test)")
    print(f"Accuracy   : {accuracy:.4f}")
    print(f"Precision  : {precision:.4f}")
    print(f"Recall     : {recall:.4f}")
    print(f"F1 Score   : {f1:.4f}")

    # --------------------
    # Sanity assertions
    # --------------------
    assert len(X_train) > 0
    assert len(X_val) > 0
    assert len(y_train) > 0
    assert len(y_val) > 0
