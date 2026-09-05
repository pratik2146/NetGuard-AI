import json
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
    auc,
    roc_auc_score
)

from netguard.config import (
    DATA_DIR,
    MODEL_DIR,
    OUTPUT_DIR,
    MODEL_PATH,
    FEATURE_PATH,
    THRESHOLD_PATH,
    COMBINED_DATA_PATH,
    MODEL_COMPARISON_PATH,
    FEATURE_IMPORTANCE_PATH,
    TEST_PREDICTIONS_PATH,
    TRAINING_SUMMARY_PATH,
    RANDOM_STATE,
    TEST_SIZE
)
from netguard.data.loader import load_raw_dataset
from netguard.data.preprocessor import (
    clean_column_names,
    process_timestamps,
    create_target_column,
    select_numeric_features,
    prepare_features
)
from netguard.models.evaluator import calculate_metrics, find_best_threshold
from netguard.utils.logger import logger

class ModelTrainer:
    """
    Model Training Pipeline for NetGuard AI.
    """
    def __init__(
        self,
        data_dir: Path = DATA_DIR,
        model_dir: Path = MODEL_DIR,
        output_dir: Path = OUTPUT_DIR
    ):
        self.data_dir = Path(data_dir)
        self.model_dir = Path(model_dir)
        self.output_dir = Path(output_dir)

        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_pipeline(self) -> Dict[str, Any]:
        """
        Execute full training, evaluation, threshold search, and artifact export flow.
        """
        logger.info("=" * 60)
        logger.info("NETGUARD AI - TRAINING PIPELINE STARTED")
        logger.info("=" * 60)

        # 1. Load Data
        df = load_raw_dataset(self.data_dir)

        # 2. Clean & Preprocess
        df = clean_column_names(df)
        df = create_target_column(df)
        df = process_timestamps(df)

        fault_count = int(df["target"].sum())
        logger.info(f"Total dataset records: {len(df):,}")
        logger.info(f"Total fault records ('class' == 'F'): {fault_count:,}")

        # 3. Feature Selection
        feature_columns = select_numeric_features(df)
        X = prepare_features(df, feature_columns)
        y = df["target"]

        # 4. Stratified Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )

        logger.info(f"Train split size: {len(X_train):,}, Test split size: {len(X_test):,}")

        # 5. Define ML Models
        models = {
            "Logistic Regression": Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced", random_state=RANDOM_STATE))
            ]),
            "Random Forest": Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("classifier", RandomForestClassifier(
                    n_estimators=300,
                    max_features="sqrt",
                    min_samples_leaf=2,
                    class_weight="balanced",
                    n_jobs=-1,
                    random_state=RANDOM_STATE
                ))
            ])
        }

        # 6. Train Models & Benchmark
        trained_models = {}
        model_probabilities = {}
        benchmark_results = []

        for name, model_pipe in models.items():
            logger.info(f"Training model: {name}...")
            model_pipe.fit(X_train, y_train)
            probs = model_pipe.predict_proba(X_test)[:, 1]

            metrics = calculate_metrics(y_test, probs, threshold=0.50)
            benchmark_results.append({"model": name, "threshold": 0.50, **metrics})

            trained_models[name] = model_pipe
            model_probabilities[name] = probs

            logger.info(
                f"  [{name}] Accuracy: {metrics['accuracy']:.4f} | Precision: {metrics['precision']:.4f} | "
                f"Recall: {metrics['recall']:.4f} | F1: {metrics['f1']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f}"
            )

        # 7. Model Comparison DataFrame
        benchmark_df = pd.DataFrame(benchmark_results).sort_values(
            by=["f1", "recall", "roc_auc"], ascending=False
        ).reset_index(drop=True)

        benchmark_df.to_csv(MODEL_COMPARISON_PATH, index=False)

        # Select Random Forest as the primary model
        selected_model_name = "Random Forest"
        selected_model = trained_models[selected_model_name]
        selected_probs = model_probabilities[selected_model_name]

        # 8. Optimal Threshold Search
        optimal_threshold, threshold_df = find_best_threshold(y_test, selected_probs)
        threshold_df.to_csv(self.output_dir / "threshold_analysis.csv", index=False)
        logger.info(f"Optimal F1-Score threshold for {selected_model_name}: {optimal_threshold:.2f}")

        # Metrics at standard and optimized thresholds
        std_metrics = calculate_metrics(y_test, selected_probs, threshold=0.50)
        opt_metrics = calculate_metrics(y_test, selected_probs, threshold=optimal_threshold)

        opt_preds = (selected_probs >= optimal_threshold).astype(int)

        # 9. Generate Plots & Reports
        self._export_confusion_matrix(y_test, opt_preds)
        self._export_classification_report(y_test, opt_preds)
        self._export_roc_and_pr_curves(y_test, selected_probs, selected_model_name)

        # 10. Feature Importance Plot & CSV
        if selected_model_name == "Random Forest":
            self._export_feature_importance(selected_model, feature_columns)

        # 11. Save Model & Feature Schema & Threshold JSON
        joblib.dump(selected_model, MODEL_PATH)

        with open(FEATURE_PATH, "w", encoding="utf-8") as f:
            json.dump(feature_columns, f, indent=2)

        with open(THRESHOLD_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "model": selected_model_name,
                "threshold": optimal_threshold,
                "selection_metric": "F1-score"
            }, f, indent=2)

        # 12. Save Test Predictions
        test_pred_df = df.loc[X_test.index, ["timestamp", "timestamp_dt", "class", "target"]].copy()
        test_pred_df["prediction_probability"] = selected_probs
        test_pred_df["prediction_standard"] = (selected_probs >= 0.50).astype(int)
        test_pred_df["prediction"] = opt_preds
        test_pred_df["risk_threshold"] = optimal_threshold
        test_pred_df.to_csv(TEST_PREDICTIONS_PATH, index=False)

        # 13. Save Combined Dataset for Dashboard
        dash_cols = ["timestamp", "timestamp_dt", "class", "target"]
        for dcol in ["Device_name", "router_name", "device_name"]:
            if dcol in df.columns:
                dash_cols.append(dcol)
        dash_cols += feature_columns
        df[dash_cols].to_csv(COMBINED_DATA_PATH, index=False)

        # 14. Save Summary JSON
        precision_curve, recall_curve, _ = precision_recall_curve(y_test, selected_probs)
        pr_auc_val = float(auc(recall_curve, precision_curve))

        summary = {
            "project": "NetGuard AI",
            "task": "Intelligent Network Fault Prediction",
            "records": int(len(df)),
            "features": int(len(feature_columns)),
            "fault_records": int(fault_count),
            "selected_model": selected_model_name,
            "standard_threshold": 0.50,
            "optimized_threshold": optimal_threshold,
            "standard_metrics": std_metrics,
            "optimized_metrics": opt_metrics,
            "pr_auc": pr_auc_val
        }

        with open(TRAINING_SUMMARY_PATH, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        logger.info("=" * 60)
        logger.info("NETGUARD AI TRAINING PIPELINE COMPLETE SUCCESSFULLY")
        logger.info(f"Saved artifacts to {self.model_dir} and {self.output_dir}")
        logger.info("=" * 60)

        return summary

    def _export_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(6, 5))
        plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
        plt.title("NetGuard AI - Confusion Matrix")
        plt.colorbar()
        plt.xlabel("Predicted Class")
        plt.ylabel("Actual Class")
        plt.xticks([0, 1], ["Non-Fault", "Fault"])
        plt.yticks([0, 1], ["Non-Fault", "Fault"])

        for i in range(2):
            for j in range(2):
                plt.text(j, i, str(cm[i, j]), ha="center", va="center", color="red" if cm[i, j] > cm.max()/2 else "black")

        plt.tight_layout()
        plt.savefig(self.output_dir / "confusion_matrix.png", dpi=200)
        plt.close()

    def _export_classification_report(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        report_text = classification_report(
            y_true, y_pred, target_names=["Non-Fault", "Fault"], zero_division=0
        )
        with open(self.output_dir / "classification_report.txt", "w", encoding="utf-8") as f:
            f.write(report_text)

    def _export_roc_and_pr_curves(self, y_true: np.ndarray, probs: np.ndarray, model_name: str) -> None:
        # ROC Curve
        fpr, tpr, _ = roc_curve(y_true, probs)
        roc_auc_val = roc_auc_score(y_true, probs)

        plt.figure(figsize=(7, 5))
        plt.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc_val:.3f})", color="#3B82F6", lw=2)
        plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("NetGuard AI - ROC Curve")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(self.output_dir / "roc_curve.png", dpi=200)
        plt.close()

        # PR Curve
        precision_curve, recall_curve, _ = precision_recall_curve(y_true, probs)
        pr_auc_val = auc(recall_curve, precision_curve)

        plt.figure(figsize=(7, 5))
        plt.plot(recall_curve, precision_curve, label=f"PR-AUC = {pr_auc_val:.3f}", color="#10B981", lw=2)
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("NetGuard AI - Precision Recall Curve")
        plt.legend(loc="lower left")
        plt.tight_layout()
        plt.savefig(self.output_dir / "precision_recall_curve.png", dpi=200)
        plt.close()

    def _export_feature_importance(self, model: Pipeline, feature_columns: List[str]) -> None:
        importances = model.named_steps["classifier"].feature_importances_
        fi_df = pd.DataFrame({"feature": feature_columns, "importance": importances})
        fi_df = fi_df.sort_values("importance", ascending=False).reset_index(drop=True)
        fi_df.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

        top20 = fi_df.head(20).sort_values("importance")
        plt.figure(figsize=(9, 7))
        plt.barh(top20["feature"], top20["importance"], color="#6366F1")
        plt.xlabel("Importance")
        plt.ylabel("Feature")
        plt.title("NetGuard AI - Top 20 Features")
        plt.tight_layout()
        plt.savefig(self.output_dir / "feature_importance.png", dpi=200)
        plt.close()
