import pytest
from src.business_rules import check_business_rules


# -----------------------------
# Helpers
# -----------------------------
def valid_base_features():
    return {
        "average_attendance_per_course": 80.0,
        "average_assignments_submission_per_course": 85.0,
        "average_test_scores_per_course": 75.0,
        "average_class_activities_and_engagements_per_course": 60.0,
    }


# -----------------------------
# OPTIONAL FEATURE TESTS
# -----------------------------
def test_allows_prediction_without_previous_semester_gpa():
    features = valid_base_features()

    result = check_business_rules(features)

    assert result["allowed"] is True
    assert result["reason"] == ""
    assert result["warnings"] == []


def test_allows_prediction_with_previous_semester_gpa_present():
    features = valid_base_features()
    features["previous_semester_gpa_scaled"] = 72.5

    result = check_business_rules(features)

    assert result["allowed"] is True
    assert result["reason"] == ""
    assert result["warnings"] == []


def test_blocks_if_previous_semester_gpa_invalid_type():
    features = valid_base_features()
    features["previous_semester_gpa_scaled"] = "bad"

    result = check_business_rules(features)

    assert result["allowed"] is False
    assert "Invalid type for previous_semester_gpa_scaled" in result["reason"]
    assert result["warnings"] == []


def test_blocks_if_previous_semester_gpa_out_of_range():
    features = valid_base_features()
    features["previous_semester_gpa_scaled"] = 150.0

    result = check_business_rules(features)

    assert result["allowed"] is False
    assert "Invalid value for previous_semester_gpa_scaled" in result["reason"]
    assert result["warnings"] == []


# -----------------------------
# REQUIRED FEATURE VALIDATION
# -----------------------------
def test_blocks_missing_required_feature():
    features = valid_base_features()
    del features["average_attendance_per_course"]

    result = check_business_rules(features)

    assert result["allowed"] is False
    assert "Missing required feature: average_attendance_per_course" == result["reason"]
    assert result["warnings"] == []


def test_blocks_invalid_type_for_required_feature():
    features = valid_base_features()
    features["average_test_scores_per_course"] = "bad"

    result = check_business_rules(features)

    assert result["allowed"] is False
    assert "Invalid type for average_test_scores_per_course" in result["reason"]
    assert result["warnings"] == []


def test_blocks_out_of_range_required_feature():
    features = valid_base_features()
    features["average_assignments_submission_per_course"] = -10

    result = check_business_rules(features)

    assert result["allowed"] is False
    assert "Invalid value for average_assignments_submission_per_course" in result["reason"]
    assert result["warnings"] == []


# -----------------------------
# BUSINESS RULES
# -----------------------------
def test_blocks_low_attendance():
    features = valid_base_features()
    features["average_attendance_per_course"] = 40.0  # below 50%

    result = check_business_rules(features)

    assert result["allowed"] is False
    assert "attendance too low" in result["reason"].lower()
    assert result["warnings"] == []


def test_warning_for_low_assignments_submission():
    features = valid_base_features()
    features["average_assignments_submission_per_course"] = 60.0

    result = check_business_rules(features)

    assert result["allowed"] is True
    assert result["reason"] == ""
    assert len(result["warnings"]) == 1
    assert "assignments submission very low" in result["warnings"][0].lower()


def test_warning_for_low_test_scores():
    features = valid_base_features()
    features["average_test_scores_per_course"] = 40.0

    result = check_business_rules(features)

    assert result["allowed"] is True
    assert result["reason"] == ""
    assert len(result["warnings"]) == 1
    assert "test scores very low" in result["warnings"][0].lower()


def test_warning_for_low_class_engagement():
    features = valid_base_features()
    features["average_class_activities_and_engagements_per_course"] = 10.0

    result = check_business_rules(features)

    assert result["allowed"] is True
    assert result["reason"] == ""
    assert len(result["warnings"]) == 1
    assert "class activities and engagements very low" in result["warnings"][0].lower()


def test_multiple_warnings_accumulate():
    features = valid_base_features()
    features["average_assignments_submission_per_course"] = 60.0
    features["average_test_scores_per_course"] = 40.0
    features["average_class_activities_and_engagements_per_course"] = 10.0

    result = check_business_rules(features)

    assert result["allowed"] is True
    assert result["reason"] == ""
    assert len(result["warnings"]) == 3
