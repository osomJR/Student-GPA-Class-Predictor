"""
Dataset utilities for the Student GPA Class Predictor.

This module:
- builds a dataset from a raw DataFrame
- applies structural contracts
- applies business rules
- converts GPA to class labels
- splits into train/validation sets
"""

from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from .schema import (
    FEATURE_ORDER,
    STRUCTURAL_CONTRACTS,
    GPA_CLASS_BOUNDARY,
    TARGET_COLUMN,
)
from .business_rules import check_business_rules


def _gpa_to_class_label(gpa_scaled: float) -> int:
    """
    Convert GPA (scaled 0-100) to class label (0-5).
    """
    gpa = gpa_scaled / 20.0  # Convert 0–100 scale to 0–5 scale

    for label, boundary in GPA_CLASS_BOUNDARY.items():
        if boundary["min_gpa"] <= gpa <= boundary["max_gpa"]:
            return label

    raise ValueError(f"Invalid GPA value: {gpa_scaled}")


def build_dataset(
    raw_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """
    Build training dataset from raw DataFrame.

    Args:
        raw_df (pd.DataFrame): Raw dataset containing input features and target column.

    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test
    """

    # Work on a copy to avoid side effects
    raw_df = raw_df.copy()

    
    # 1. Clean column names (CRITICAL FIX)
    
    raw_df.columns = raw_df.columns.str.strip()

    
    # 2. Validate required columns exist
    
    missing_columns = set(FEATURE_ORDER) - set(raw_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Keep only required columns
    raw_df = raw_df[FEATURE_ORDER]

    
    # 3. Structural contract validation
    
    for feature_name, contract in STRUCTURAL_CONTRACTS.items():
        min_val = contract["min"]
        max_val = contract["max"]

        if not raw_df[feature_name].between(min_val, max_val).all():
            raise ValueError(
                f"Feature '{feature_name}' out of range. "
                f"Expected between {min_val} and {max_val}."
            )

    
    # 4. Apply business rules
    
    valid_rows = []
    for _, row in raw_df.iterrows():
        result = check_business_rules(row.to_dict())
        if result["allowed"]:
            valid_rows.append(row)

    if not valid_rows:
        raise ValueError(
            "No valid rows found after applying business rules."
        )

    valid_df = pd.DataFrame(valid_rows)

    
    # 5. Convert GPA to class label

    valid_df[TARGET_COLUMN] = valid_df[
        "previous_semester_gpa_scaled"
    ].apply(_gpa_to_class_label)

    
    # 6. Split features and target
    
    X = valid_df.drop(
        columns=["previous_semester_gpa_scaled", TARGET_COLUMN]
    )
    y = valid_df[TARGET_COLUMN]

    
    # 7. Train / validation / test split (60/20/20)

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.4,   # 40% -> validation + test
        random_state=42,
        stratify=y,
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.5,   # split 40% into 20% val and 20% test
        random_state=42,
        stratify=y_temp,
    )

    return X_train, X_val, X_test, y_train, y_val, y_test
