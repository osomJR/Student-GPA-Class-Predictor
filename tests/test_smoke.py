import pandas as pd
from src.dataset import build_dataset

raw_df = pd.read_csv("data/raw/student_records.csv")

# Use a small subset for smoke testing
raw_df = raw_df.sample(n=500, random_state=42)

X_train, X_val, y_train, y_val = build_dataset(raw_df)

print("Smoke test PASSED with real data")
