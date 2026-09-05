import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple
import joblib
import numpy as np
import pandas as pd

from netguard.config import (
    MODEL_PATH, 
    FEATURE_PATH, 
    THRESHOLD_PATH, 
    DEFAULT_THRESHOLD,
    RISK_LEVELS
)
from netguard.data.preprocessor import prepare_features
from netguard.utils.logger import logger

class NetGuardPredictor:
    """
    Inference Engine for NetGuard AI fault risk prediction.
    """
    def __init__(
        self,
        model_path: Union[str, Path] = MODEL_PATH,
        feature_path: Union[str, Path] = FEATURE_PATH,
        threshold_path: Union[str, Path] = THRESHOLD_PATH,
    ):
        self.model_path = Path(model_path)
        self.feature_path = Path(feature_path)
        self.threshold_path = Path(threshold_path)

        self.model = None
        self.features: List[str] = []
        self.threshold: float = DEFAULT_THRESHOLD

        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """Load model binary, feature schema, and optimal threshold."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        if not self.feature_path.exists():
            raise FileNotFoundError(f"Feature schema file not found: {self.feature_path}")

        logger.info(f"Loading trained ML model from {self.model_path}")
        self.model = joblib.load(self.model_path)

        with open(self.feature_path, "r", encoding="utf-8") as f:
            self.features = json.load(f)

        if self.threshold_path.exists():
            try:
                with open(self.threshold_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.threshold = float(data.get("threshold", DEFAULT_THRESHOLD))
            except Exception as e:
                logger.warning(f"Could not load optimal threshold: {e}. Using default {DEFAULT_THRESHOLD}")
                self.threshold = DEFAULT_THRESHOLD
        else:
            self.threshold = DEFAULT_THRESHOLD

        logger.info(f"Predictor initialized with {len(self.features)} features and threshold {self.threshold:.2f}")

    def get_risk_info(self, probability: float) -> Dict[str, Any]:
        """
        Map a predicted fault probability to risk level metadata.
        """
        if probability >= 0.80:
            level = "CRITICAL"
        elif probability >= 0.60:
            level = "HIGH"
        elif probability >= 0.30:
            level = "MEDIUM"
        else:
            level = "LOW"

        meta = RISK_LEVELS[level]
        return {
            "risk_level": level,
            "emoji": meta["emoji"],
            "badge": meta["badge"],
            "advice": meta["advice"],
        }

    def predict_dataframe(self, df: pd.DataFrame) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Perform model prediction on a pandas DataFrame.
        Returns:
            Tuple of (probabilities array, risk info list)
        """
        X = prepare_features(df, self.features)
        probabilities = self.model.predict_proba(X)[:, 1]
        risk_info_list = [self.get_risk_info(p) for p in probabilities]
        return probabilities, risk_info_list

    def predict_single(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform model prediction on a single record dictionary.
        """
        single_df = pd.DataFrame([input_dict])
        probs, risks = self.predict_dataframe(single_df)
        prob = float(probs[0])
        risk_info = risks[0]

        return {
            "fault_probability": prob,
            "fault_probability_percent": round(prob * 100, 2),
            "is_fault_predicted": bool(prob >= self.threshold),
            "risk_threshold": self.threshold,
            **risk_info
        }
