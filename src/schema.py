"""
Data schema definitions for the Student GPA Class predictor.
This module defines:
- Input features, type and valid ranges
- GPA class boundaries and label encoding
- Confidence, attendance, assignments submission, test scores, class activities and engagements thresholds
- Feature ordering and structural contracts
"""
from dataclasses import dataclass
from typing import Dict, List
# Input Features, type and valid ranges
INPUT_FEATURES = {
    "average_attendance_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "description": "average percentage of all classes attended punctually"
    },
    "average_assignments_submission_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "description": "average percentage of all assignments submitted on time"
    },
    "average_test_scores_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "description": "avaerage percentage of all test scores"
    },
    "average_class_activities_and_engagements_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "description": "average percentage of all class activities and engagements"
    },
    "previous_semester_gpa_scaled": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "description": "percentage of previous semester gpa"
    }
}
# GPA class boundaries and label encoding
GPA_CLASS_BOUNDARY = {
    0: {"name": "First Class", "min_gpa": 4.5000, "max_gpa": 5.0000},
    1: {"name": "Second Class Upper", "min_gpa": 3.5000, "max_gpa": 4.4999},
    2: {"name": "Second Class Lower", "min_gpa": 2.5000, "max_gpa": 3.4999},
    3: {"name": "Third Class", "min_gpa": 2.0000, "max_gpa": 2.4999},
    4: {"name": "Pass", "min_gpa": 1.5000, "max_gpa": 1.9999},
    5: {"name": "Fail", "min_gpa": 0.0000, "max_gpa": 1.4999},
}
# Target column for classification
TARGET_COLUMN = "gpa_class_label"
# Confidence, attendance, assignments submission, test scores, class activities and engagements thresholds
CONFIDENCE_THRESHOLD: float = 0.6500
"""
Minimum predicted probability required for a GPA class prediction to be considered high-confidence. Predictions below this threshold remain valid but must be flagged for review by the level advisor.
"""

ATTENDANCE_THRESHOLD: float = 0.5000
"""
Proportion of class duration which a student is punctual and given attendance. Students who fall short of this duration are regarded absent like they never attended the class.
"""

ASSIGNMENTS_SUBMISSION_THRESHOLD: float = 0.7000
"""
Submitted asssignments must be at least the threshold value
"""

TEST_SCORES_THRESHOLD: float = 0.4500
"""
Test scores must be at least the threshold value
"""

CLASS_ACTIVITIES_AND_ENGAGEMENTS_THRESHOLD: float = 0.2000
"""
Minimum value which is regarded an active class member
"""
# Feature ordering and structural contracts
FEATURE_ORDER = [
    "average_attendance_per_course",
    "average_assignments_submission_per_course",
    "average_test_scores_per_course",
    "average_class_activities_and_engagements_per_course",
    "previous_semester_gpa_scaled",
]

STRUCTURAL_CONTRACTS = {
    "average_attendance_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "required": True,
    },
    "average_assignments_submission_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "required": True,
    },
    "average_test_scores_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "required": True,
    },
    "average_class_activities_and_engagements_per_course": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "required": True,
    },
    "previous_semester_gpa_scaled": {
        "type": "numeric",
        "min":0.0,
        "max":100.0,
        "required": True,
    },
}











