"""
Labeling logic for the Student GPA Class Predictor.

Converts validated student features into GPA class labels based on schema.
"""

from typing import Dict, Tuple
from .schema import GPA_CLASS_BOUNDARY


def assign_gpa_class(predicted_gpa: float) -> Tuple[int, str]:
    """
    Assigns a GPA class based on predicted GPA value.

    Args:
        predicted_gpa (float): GPA value (0.0-5.0)

    Returns:
        Tuple[int, str]: (class_index, class_name)
    """
    for idx, boundary in GPA_CLASS_BOUNDARY.items():
        if boundary["min_gpa"] <= predicted_gpa <= boundary["max_gpa"]:
            return idx, boundary["name"]

    raise ValueError(f"GPA value {predicted_gpa} is out of bounds.")


def label_student(features: Dict[str, float], predicted_gpa: float) -> Dict[str, str]:
    """
    Creates a labeled output for a student.

    Args:
        features (Dict[str, float]): Validated input features
        predicted_gpa (float): Predicted GPA value

    Returns:
        Dict[str, str]: Features with additional 'gpa_class' info
    """
    class_idx, class_name = assign_gpa_class(predicted_gpa)
    labeled_output = features.copy()
    labeled_output.update({
        "gpa_class_index": class_idx,
        "gpa_class_name": class_name
    })
    return labeled_output
