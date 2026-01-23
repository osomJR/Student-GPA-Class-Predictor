"""
Business rule enforcement for the Student GPA Class Predictor
This module enforces academic and policy eligibility rules that determine whether a student's data is eligible for GPA prediction.
"""

from typing import Dict, List
from .schema import (
    ATTENDANCE_THRESHOLD,
    ASSIGNMENTS_SUBMISSION_THRESHOLD,
    TEST_SCORES_THRESHOLD,
    CLASS_ACTIVITIES_AND_ENGAGEMENTS_THRESHOLD,
    STRUCTURAL_CONTRACTS,
)

# Feature that is OPTIONAL and IGNORED by business rules
OPTIONAL_IGNORED_FEATURE = "previous_semester_gpa_scaled"


def check_business_rules(features: Dict[str, float]) -> Dict[str, object]:
    """
    Checks whether a student's features meet academic eligibility criteria.
    """

    warnings: List[str] = []

    # -----------------------------
    # Input validation
    # -----------------------------
    for feature_name, contract in STRUCTURAL_CONTRACTS.items():

        # 🔹 previous_semester_gpa_scaled is OPTIONAL
        if feature_name == OPTIONAL_IGNORED_FEATURE:
            if feature_name not in features:
                continue  # absence is allowed

            value = features[feature_name]

            # validate type and range ONLY if provided
            if not isinstance(value, (int, float)):
                return {
                    "allowed": False,
                    "reason": f"Invalid type for {feature_name}. Expected numeric value.",
                    "warnings": [],
                }

            if value < contract["min"] or value > contract["max"]:
                return {
                    "allowed": False,
                    "reason": (
                        f"Invalid value for {feature_name}. "
                        f"Expected between {contract['min']} and {contract['max']}. "
                        f"Received {value}."
                    ),
                    "warnings": [],
                }

            continue  # do NOT enforce further rules on it

        # -----------------------------
        # Normal required features
        # -----------------------------
        if feature_name not in features:
            return {
                "allowed": False,
                "reason": f"Missing required feature: {feature_name}",
                "warnings": [],
            }

        value = features[feature_name]

        if not isinstance(value, (int, float)):
            return {
                "allowed": False,
                "reason": f"Invalid type for {feature_name}. Expected numeric value.",
                "warnings": [],
            }

        if value < contract["min"] or value > contract["max"]:
            return {
                "allowed": False,
                "reason": (
                    f"Invalid value for {feature_name}. "
                    f"Expected between {contract['min']} and {contract['max']}. "
                    f"Received {value}."
                ),
                "warnings": [],
            }

    # -----------------------------
    # Business rules (current semester only)
    # -----------------------------
    attendance_ratio = features["average_attendance_per_course"] / 100.0
    assignments_submission_ratio = features["average_assignments_submission_per_course"] / 100.0
    test_scores_ratio = features["average_test_scores_per_course"] / 100.0
    class_activities_and_engagements_ratio = features["average_class_activities_and_engagements_per_course"] / 100.0

    # Attendance rule (blocking)
    if attendance_ratio < ATTENDANCE_THRESHOLD:
        return {
            "allowed": False,
            "reason": "Student attendance too low to compute GPA, advised to see the Dean with his or her parents/guardian.",
            "warnings": [],
        }

    # Assignments submission rule (warning only)
    if assignments_submission_ratio < ASSIGNMENTS_SUBMISSION_THRESHOLD:
        warnings.append(
            "Student assignments submission very low, advised to see the Dean with his or her parents/guardian."
        )

    # Test scores rule (warning only)
    if test_scores_ratio < TEST_SCORES_THRESHOLD:
        warnings.append(
            "Student test scores very low, advised to see the Dean with his or her parents/guardian."
        )

    # Class activities and engagements rule (warning only)
    if class_activities_and_engagements_ratio < CLASS_ACTIVITIES_AND_ENGAGEMENTS_THRESHOLD:
        warnings.append(
            "Student class activities and engagements very low, advised to see the Dean with his or her parents/guardian."
        )

    return {
        "allowed": True,
        "reason": "",
        "warnings": warnings,
    }
