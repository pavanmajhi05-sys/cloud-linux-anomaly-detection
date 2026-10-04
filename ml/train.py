import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


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


def train_model():
    print("Loading ML dataset...")

    df = pd.read_csv(INPUT_FILE)

    # Train only on known normal observations.
    normal_data = df[df["label"] == 0]

    X_train = normal_data[FEATURES]

    print(f"Total samples: {len(df)}")
    print(f"Normal training samples: {len(X_train)}")
    print(f"Known anomaly samples: {len(df[df['label'] == 1])}")

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train)

    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)

    joblib.dump(model, MODEL_FILE)

    print("\nModel training completed successfully.")
    print(f"Model saved to: {MODEL_FILE}")


if __name__ == "__main__":
    train_model()
