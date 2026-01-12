import sys
import os

# Add src/ to Python path explicitly
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_PATH)

from src.validation import validate_input


# Valid test input (MUST follow FEATURE_ORDER)
valid_input = {
    "average_attendance_per_course": 85.0,
    "average_assignments_submission_per_course": 90.0,
    "average_test_scores_per_course": 78.0,
    "average_class_activities_and_engagements": 88.0,
    "previous_semester_gpa_scaled": 72.0,
}

try:
    validated = validate_input(valid_input)
    print("Validation PASSED")
    print("Validated input:", validated)

except ValueError as e:
    print("Validation FAILED")
    print("Error:", e)
