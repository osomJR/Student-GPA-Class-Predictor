from typing import Dict, List
from .schema import FEATURE_ORDER


def preprocess_input(features: Dict[str, float]) -> List[float]:
    ordered_features = _order_features(features)
    return _scale_features(ordered_features)


def _order_features(features: Dict[str, float]) -> List[float]:
    try:
        return [features[feature_name] for feature_name in FEATURE_ORDER]
    except KeyError as e:
        raise KeyError(
            f"Missing feature during preprocessing: {e.args[0]}"
        )


def _scale_features(feature_values: List[float]) -> List[float]:
    return [float(value) / 100.0 for value in feature_values]



