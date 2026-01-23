import sys
import os

# Add src/ to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "..", "src")
sys.path.insert(0, SRC_PATH)

from src.labeling import label_student

# Example validated input (matches FEATURE_ORDER)
valid_input = {
    "average_attendance_per_course": 85.0,
    "average_assignments_submission_per_course": 90.0,
    "average_test_scores_per_course": 78.0,
    "average_class_activities_and_engagements_per_course": 88.0,
    "previous_semester_gpa_scaled": 72.0,
}

# Example predicted GPA for testing
predicted_gpa = 4.2  # Should correspond to "Second Class Upper"

try:
    labeled_output = label_student(valid_input, predicted_gpa)
    print("Labeling PASSED")
    print("Labeled output:", labeled_output)

except ValueError as e:
    print("Labeling FAILED")
    print("Error:", e)
