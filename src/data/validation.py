"""
Validation logic for the Student GPA Class Predictor.

This module enforces:
- Structural contracts
- Feature presence
- Feature order
- Data types
- Value ranges
- Attendance business rules
"""

from typing import Dict
from schema import (
    STRUCTURAL_CONTRACTS,
    FEATURE_ORDER,
    ATTENDANCE_THRESHOLD,
)


# ==================================================
# Public Validation Function
# ==================================================

def validate_input(features: Dict[str, float]) -> Dict[str, float]:
    """
    Validates input features against schema-defined rules.

    Args:
        features (dict): Input feature dictionary

    Returns:
        dict: Validated feature dictionary

    Raises:
        ValueError: If any validation rule fails
    """
    _validate_required_features(features)
    _validate_no_extra_features(features)
    _validate_feature_order(features)
    _validate_types(features)
    _validate_ranges(features)
    _validate_attendance_threshold(features)

    return features


# ==================================================
# Feature Presence Validation
# ==================================================

def _validate_required_features(features: Dict[str, float]) -> None:
    missing_features = [
        feature
        for feature, spec in STRUCTURAL_CONTRACTS.items()
        if spec.get("required") and feature not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required input features: {missing_features}"
        )


def _validate_no_extra_features(features: Dict[str, float]) -> None:
    extra_features = [
        feature for feature in features
        if feature not in STRUCTURAL_CONTRACTS
    ]

    if extra_features:
        raise ValueError(
            f"Unexpected input features provided: {extra_features}"
        )


# ==================================================
# Feature Order Validation
# ==================================================

def _validate_feature_order(features: Dict[str, float]) -> None:
    if list(features.keys()) != FEATURE_ORDER:
        raise ValueError(
            "Input feature order does not match schema definition. "
            f"Expected order: {FEATURE_ORDER}"
        )


# ==================================================
# Data Type Validation
# ==================================================

def _validate_types(features: Dict[str, float]) -> None:
    for feature_name, value in features.items():
        expected_type = STRUCTURAL_CONTRACTS[feature_name]["type"]

        if expected_type == "numeric":
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"Feature '{feature_name}' must be numeric. "
                    f"Received type: {type(value).__name__}"
                )


# ==================================================
# Range Validation
# ==================================================

def _validate_ranges(features: Dict[str, float]) -> None:
    for feature_name, value in features.items():
        spec = STRUCTURAL_CONTRACTS[feature_name]

        min_value = spec.get("min")
        max_value = spec.get("max")

        if min_value is not None and value < min_value:
            raise ValueError(
                f"Feature '{feature_name}' is below minimum allowed "
                f"({value} < {min_value})"
            )

        if max_value is not None and value > max_value:
            raise ValueError(
                f"Feature '{feature_name}' exceeds maximum allowed "
                f"({value} > {max_value})"
            )


# ==================================================
# Attendance Business Rule
# ==================================================

def _validate_attendance_threshold(features: Dict[str, float]) -> None:
    attendance_percentage = features.get(
        "average_attendance_per_course"
    )

    if attendance_percentage is not None:
        attendance_ratio = attendance_percentage / 100.0

        if attendance_ratio < ATTENDANCE_THRESHOLD:
            raise ValueError(
                "Attendance below acceptable threshold. "
                f"({attendance_ratio:.2f} < {ATTENDANCE_THRESHOLD})"
            )
