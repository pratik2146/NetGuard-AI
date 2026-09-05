from typing import Dict, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    auc,
    precision_recall_curve
)

def calculate_metrics(
    y_true: np.ndarray, 
    probabilities: np.ndarray, 
    threshold: float = 0.50
) -> Dict[str, float]:
    """
    Calculate classification performance metrics given predicted probabilities and decision threshold.
    """
    predictions = (probabilities >= threshold).astype(int)
    
    acc = accuracy_score(y_true, predictions)
    prec = precision_score(y_true, predictions, zero_division=0)
    rec = recall_score(y_true, predictions, zero_division=0)
    f1 = f1_score(y_true, predictions, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y_true, probabilities)
    except ValueError:
        roc_auc = 0.0

    return {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1": float(f1),
        "roc_auc": float(roc_auc)
    }

def find_best_threshold(
    y_true: np.ndarray, 
    probabilities: np.ndarray,
    min_thresh: float = 0.10,
    max_thresh: float = 0.90,
    step: float = 0.01
) -> Tuple[float, pd.DataFrame]:
    """
    Grid search to find optimal decision threshold maximizing F1-score.
    """
    thresholds = np.arange(min_thresh, max_thresh + step, step)
    rows = []
    
    for th in thresholds:
        preds = (probabilities >= th).astype(int)
        p = precision_score(y_true, preds, zero_division=0)
        r = recall_score(y_true, preds, zero_division=0)
        f = f1_score(y_true, preds, zero_division=0)
        rows.append({
            "threshold": round(float(th), 2),
            "precision": float(p),
            "recall": float(r),
            "f1": float(f)
        })
        
    df_thresh = pd.DataFrame(rows)
    best_row = df_thresh.loc[df_thresh["f1"].idxmax()]
    best_threshold = float(best_row["threshold"])
    
    return best_threshold, df_thresh
