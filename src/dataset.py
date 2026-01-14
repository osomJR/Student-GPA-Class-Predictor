"""
Dataset utilities for the Student GPA Class Predictor.

- Loads raw student data
- Cleans column names
- Validates features
- Preprocesses features
- Splits into train/validation sets
"""

from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split

from .validation import validate_input
from .preprocessing import preprocess_input
from .labeling import label_student

def build_dataset(raw_df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
                 ) -> Tuple[list, list, list, list]:
    """
    Builds dataset ready for model training and evaluation.

    Args:
        raw_df (pd.DataFrame): Raw student data
        test_size (float): Fraction of data for validation
        random_state (int): Random seed

    Returns:
        Tuple: X_train, X_val, y_train, y_val (all as lists of preprocessed features)
    """

    # 1. Strip column whitespace
    raw_df.columns = raw_df.columns.str.strip()

    # 2. Rename student column if needed
    if 'Student' in raw_df.columns:
        raw_df = raw_df.rename(columns={'Student': 'student_id'})

    X = []
    y = []

    # 3. Loop through each row for validation, preprocessing, and labeling
    for _, row in raw_df.iterrows():
        # Convert row to dict
        features = row.to_dict()

        # 3a. Validate features
        validated_features = validate_input(features)

        # 3b. Preprocess input (scales values to 0-1)
        X_row = preprocess_input(validated_features)
        X.append(X_row)

        # 3c. Label student using predicted GPA
        # Here we assume 'previous_semester_gpa_scaled' as the predicted GPA scaled
        predicted_gpa = validated_features['previous_semester_gpa_scaled'] / 20  # Convert 0-100 to 0-5 scale
        labeled = label_student(validated_features, predicted_gpa)
        y.append(labeled['gpa_class_index'])  # You can also store class_name if desired

    # 4. Split into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True
    )

    return X_train, X_val, y_train, y_val

