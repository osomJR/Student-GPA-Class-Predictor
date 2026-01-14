import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "..", "src")
sys.path.insert(0, SRC_PATH)

from src.preprocessing import preprocess_input


def test_preprocessing():
    valid_input = {
        "average_attendance_per_course": 80.0,
        "average_assignments_submission_per_course": 90.0,
        "average_test_scores_per_course": 70.0,
        "average_class_activities_and_engagements": 85.0,
        "previous_semester_gpa_scaled": 75.0,
    }

    processed = preprocess_input(valid_input)

    assert len(processed) == 5
    assert all(0.0 <= value <= 1.0 for value in processed)


if __name__ == "__main__":
    test_preprocessing()
    print("Preprocessing tests PASSED")


