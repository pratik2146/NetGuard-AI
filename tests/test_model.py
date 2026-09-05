import numpy as np
import pandas as pd
from netguard.models.evaluator import calculate_metrics, find_best_threshold
from netguard.models.predictor import NetGuardPredictor
from netguard.config import MODEL_PATH

def test_calculate_metrics():
    y_true = np.array([0, 1, 1, 0])
    probs = np.array([0.1, 0.9, 0.8, 0.2])
    metrics = calculate_metrics(y_true, probs, threshold=0.50)
    assert metrics["accuracy"] == 1.0
    assert metrics["f1"] == 1.0

def test_find_best_threshold():
    y_true = np.array([0, 0, 1, 1, 1])
    probs = np.array([0.1, 0.2, 0.65, 0.70, 0.90])
    best_th, thresh_df = find_best_threshold(y_true, probs)
    assert 0.20 <= best_th <= 0.65
    assert not thresh_df.empty

def test_predictor_initialization():
    if MODEL_PATH.exists():
        predictor = NetGuardPredictor()
        assert predictor.model is not None
        assert len(predictor.features) > 0

        sample_input = {feat: 0.0 for feat in predictor.features}
        res = predictor.predict_single(sample_input)
        assert "fault_probability" in res
        assert "risk_level" in res
