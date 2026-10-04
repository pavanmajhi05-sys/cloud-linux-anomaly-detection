import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

DATASET = "dataset/processed/clean_combined_anomaly_dataset.csv"
MODEL_PATH = "ml/model/isolation_forest_clean.joblib"
RESULTS_PATH = "dataset/processed/clean_experiment_results.csv"

FEATURES = [
    "cpu",
    "memory",
    "disk",
    "network_in_rate",
    "network_out_rate",
    "disk_read_rate",
    "disk_write_rate",
    "load",
    "process_count",
]


def main():

    print("=" * 70)
    print("CLEAN CPU + DISK-I/O ISOLATION FOREST EXPERIMENT")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------

    print("\nLoading dataset...")

    df = pd.read_csv(DATASET)

    print(f"Total samples      : {len(df)}")
    print(
        f"Normal samples     : "
        f"{(df['label'] == 0).sum()}"
    )
    print(
        f"Anomaly samples    : "
        f"{(df['label'] == 1).sum()}"
    )

    print("\nAnomaly types:")
    print(df[df["label"] == 1]["anomaly_type"].value_counts())

    # ---------------------------------------------------------
    # Separate normal and anomaly data
    # ---------------------------------------------------------

    normal = df[df["label"] == 0].copy()
    anomalies = df[df["label"] == 1].copy()

    # ---------------------------------------------------------
    # Train/test split
    # ---------------------------------------------------------

    # Use 80% of normal data for training.
    # Keep 20% unseen normal data for testing.
    normal_train = normal.sample(
        frac=0.8,
        random_state=42
    )

    normal_test = normal.drop(
        normal_train.index
    )

    test = pd.concat(
        [normal_test, anomalies],
        ignore_index=True
    )

    print("\nTrain/test split:")
    print(f"Training normal samples : {len(normal_train)}")
    print(f"Unseen normal samples   : {len(normal_test)}")
    print(f"Known anomalies         : {len(anomalies)}")
    print(f"Total test samples      : {len(test)}")

    # ---------------------------------------------------------
    # Prepare features
    # ---------------------------------------------------------

    X_train = normal_train[FEATURES]
    X_test = test[FEATURES]

    y_test = test["label"]

    # ---------------------------------------------------------
    # Train Isolation Forest
    # ---------------------------------------------------------

    print("\nTraining Isolation Forest...")

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train)

    print("Training completed.")

    # ---------------------------------------------------------
    # Save model
    # ---------------------------------------------------------

    import os
    import joblib

    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print(f"Model saved to: {MODEL_PATH}")

    # ---------------------------------------------------------
    # Predictions
    # ---------------------------------------------------------

    print("\nRunning predictions...")

    raw_predictions = model.predict(X_test)

    # Isolation Forest:
    # +1 = normal
    # -1 = anomaly
    predictions = [
        1 if prediction == -1 else 0
        for prediction in raw_predictions
    ]

    test["prediction"] = predictions

    # ---------------------------------------------------------
    # Overall metrics
    # ---------------------------------------------------------

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    print("\n" + "=" * 70)
    print("OVERALL RESULTS")
    print("=" * 70)

    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nConfusion Matrix:")
    print(matrix)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["Normal", "Anomaly"],
            zero_division=0
        )
    )

    # ---------------------------------------------------------
    # Error analysis
    # ---------------------------------------------------------

    tn, fp, fn, tp = matrix.ravel()

    print("=" * 70)
    print("ERROR ANALYSIS")
    print("=" * 70)

    print(f"True Negatives  : {tn}")
    print(f"False Positives : {fp}")
    print(f"False Negatives : {fn}")
    print(f"True Positives  : {tp}")

    # ---------------------------------------------------------
    # Anomaly-type analysis
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("ANOMALY-TYPE ANALYSIS")
    print("=" * 70)

    for anomaly_type in [
        "cpu_anomaly",
        "disk_io_anomaly"
    ]:

        subset = test[
            test["anomaly_type"] == anomaly_type
        ]

        if len(subset) == 0:
            continue

        actual = subset["label"]
        predicted = subset["prediction"]

        type_precision = precision_score(
            actual,
            predicted,
            zero_division=0
        )

        type_recall = recall_score(
            actual,
            predicted,
            zero_division=0
        )

        type_f1 = f1_score(
            actual,
            predicted,
            zero_division=0
        )

        detected = int(
            (predicted == 1).sum()
        )

        missed = int(
            (predicted == 0).sum()
        )

        print(f"\n{anomaly_type}:")
        print(f"Samples detected : {detected}")
        print(f"Samples missed   : {missed}")
        print(f"Precision        : {type_precision:.4f}")
        print(f"Recall           : {type_recall:.4f}")
        print(f"F1 Score         : {type_f1:.4f}")

    # ---------------------------------------------------------
    # Known anomaly predictions
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("KNOWN ANOMALY PREDICTIONS")
    print("=" * 70)

    anomaly_results = test[
        test["label"] == 1
    ][
        [
            "timestamp",
            "anomaly_type",
            "cpu",
            "memory",
            "disk",
            "disk_read_rate",
            "disk_write_rate",
            "load",
            "prediction",
        ]
    ]

    print(
        anomaly_results.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # Save detailed results
    # ---------------------------------------------------------

    test.to_csv(
        RESULTS_PATH,
        index=False
    )

    print(
        f"\nDetailed results saved to: "
        f"{RESULTS_PATH}"
    )

    print("\nExperiment completed successfully.")


if __name__ == "__main__":
    main()
