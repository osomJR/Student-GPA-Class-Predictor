import random
from typing import Dict, List


# CLASS-LEVEL FEEDBACK
CLASS_FEEDBACK = {
    "First Class": [
        "This is an outstanding academic achievement.",
        "Excellent performance, you are operating at the highest academic level.",
        "You have demonstrated exceptional consistency and mastery.",
        "Top-tier performance, keep sustaining this momentum."
    ],
    "Second Class Upper": [
        "This is a strong academic performance.",
        "You are performing above average with good consistency.",
        "Very good results, pushing slightly harder can yield First Class.",
    ],
    "Second Class Lower": [
        "This is a moderate academic performance with room for growth.",
        "There is potential for stronger academic outcomes.",
        "Improvement in key areas can significantly raise performance."
    ],
    "Third Class": [
        "Performance indicates academic difficulties.",
        "Greater focus and structured study habits are needed.",
        "There are noticeable gaps that require attention."
    ],
    "Pass": [
        "Minimum academic requirements are met.",
        "Significant improvement is necessary for future success.",
        "This performance suggests serious academic challenges."
    ],
    "Fail": [
        "Performance falls below acceptable academic standards.",
        "Immediate academic intervention is strongly recommended.",
        "A major change in study approach is required."
    ]
}


# FEATURE-LEVEL FEEDBACK

FEATURE_FEEDBACK = {
    "attendance": {
        "high": [
            "Class attendance is excellent and contributes positively to learning.",
            "Strong attendance shows commitment to academic success.",
            "Being present consistently has supported your performance."
        ],
        "medium": [
            "Attendance is fair but can be improved.",
            "More consistent class participation may boost understanding.",
        ],
        "low": [
            "Low attendance may negatively affect comprehension.",
            "Improving attendance should be a top priority.",
            "Frequent absence can hinder academic progress."
        ]
    },
    "tests": {
        "high": [
            "Test performance is strong and reflects good understanding.",
            "You demonstrate solid mastery in assessments.",
        ],
        "medium": [
            "Test scores are moderate but can be strengthened.",
            "Better revision strategies may improve results."
        ],
        "low": [
            "Test performance indicates weak understanding.",
            "More preparation is needed before assessments.",
            "Focused study is required to improve test outcomes."
        ]
    },
    "assignments": {
        "high": [
            "Assignment submission rate is excellent.",
            "Timely submissions show strong academic responsibility."
        ],
        "medium": [
            "Assignment completion is fair but inconsistent.",
            "Improving submission consistency will help performance."
        ],
        "low": [
            "Low assignment submission affects overall performance.",
            "Better time management is needed for assignments.",
            "Incomplete assignments reduce academic outcomes."
        ]
    },
    "engagement": {
        "high": [
            "Class participation is commendable.",
            "Active engagement enhances learning outcomes."
        ],
        "medium": [
            "Class engagement is moderate but could increase.",
            "More participation may deepen understanding."
        ],
        "low": [
            "Low class engagement limits learning opportunities.",
            "Participating more actively can improve performance."
        ]
    }
}


# PERFORMANCE BANDING

def categorize(value: float) -> str:
    if value >= 75:
        return "high"
    elif value >= 50:
        return "medium"
    return "low"



# FEEDBACK GENERATOR


def generate_feedback(predicted_class: str, features: Dict[str, float]) -> str:
    feedback_parts: List[str] = []

    # Class feedback
    feedback_parts.append(random.choice(CLASS_FEEDBACK[predicted_class]))

    mapping = {
        "average_attendance_per_course": "attendance",
        "average_test_scores_per_course": "tests",
        "average_assignments_submission_per_course": "assignments",
        "average_class_activities_and_engagements_per_course": "engagement"
    }

    strengths = []
    weaknesses = []

    # Analyze strengths & weaknesses
    for feature, category in mapping.items():
        level = categorize(features[feature])
        sentence = random.choice(FEATURE_FEEDBACK[category][level])
        feedback_parts.append(sentence)

        if level == "high":
            strengths.append(category)
        elif level == "low":
            weaknesses.append(category)

    # Personalized contrast logic
    if predicted_class in ["First Class", "Second Class Upper"] and weaknesses:
        feedback_parts.append(
            f"Despite strong overall results, improvement in {', '.join(weaknesses)} could further strengthen academic standing."
        )

    if predicted_class in ["Pass", "Fail", "Third Class"] and strengths:
        feedback_parts.append(
            f"However, strengths in {', '.join(strengths)} show clear potential for academic improvement."
        )

    # Personalized encouragement
    if predicted_class == "First Class":
        feedback_parts.append("Maintaining consistency across all performance areas will help sustain this excellence.")

    if predicted_class == "Fail":
        feedback_parts.append("With structured support and focused effort, academic recovery is achievable.")

    return " ".join(feedback_parts)
