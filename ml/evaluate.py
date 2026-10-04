import joblib
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


INPUT_FILE = "dataset/processed/ml_features.csv"
MODEL_FILE = "ml/model/isolation_forest.joblib"

FEATURES = [
    "cpu",
    "memory",
    "disk",
    "network_in_rate",
    "network_out_rate",
    "load",
    "process_count",
]


def evaluate_model():
    print("Loading dataset and model...")

    df = pd.read_csv(INPUT_FILE)
    model = joblib.load(MODEL_FILE)

    X = df[FEATURES]
    y_true = df["label"]

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly
    raw_predictions = model.predict(X)

    # Convert to our label format:
    # 0 = normal
    # 1 = anomaly
    y_pred = (raw_predictions == -1).astype(int)

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print("\n=== MODEL EVALUATION ===")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")

    print("\n=== CONFUSION MATRIX ===")
    print("Rows = actual, Columns = predicted")
    print(confusion_matrix(y_true, y_pred))

    print("\n=== CLASSIFICATION REPORT ===")
    print(
        classification_report(
            y_true,
            y_pred,
            target_names=["Normal", "Anomaly"],
            zero_division=0,
        )
    )

    print("\n=== DETECTED ANOMALIES ===")
    detected = df[y_pred == 1].copy()

    if detected.empty:
        print("No anomalies detected.")
    else:
        detected["prediction"] = 1
        print(
            detected[
                ["cpu", "memory", "load", "process_count", "label", "prediction"]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    evaluate_model()
