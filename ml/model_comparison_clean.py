import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


DATASET = "dataset/processed/clean_combined_anomaly_dataset.csv"

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


def evaluate_model(name, model, X_train, X_test, y_test):
    print(f"\n{'=' * 70}")
    print(name)
    print("=" * 70)

    model.fit(X_train)

    raw_predictions = model.predict(X_test)

    # Isolation Forest / One-Class SVM:
    # +1 = normal, -1 = anomaly
    # LOF with novelty=True behaves the same way.
    predictions = [
        1 if p == -1 else 0
        for p in raw_predictions
    ]

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

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions
    ).ravel()

    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"False Positives : {fp}")
    print(f"False Negatives : {fn}")

    return {
        "model": name,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positives": fp,
        "false_negatives": fn,
    }


def main():

    print("=" * 70)
    print("CLEAN ML MODEL COMPARISON")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------

    df = pd.read_csv(DATASET)

    print(f"\nTotal samples : {len(df)}")

    normal = df[df["label"] == 0].copy()
    anomalies = df[df["label"] == 1].copy()

    print(f"Normal samples  : {len(normal)}")
    print(f"Anomaly samples : {len(anomalies)}")

    # ---------------------------------------------------------
    # Same split for every model
    # ---------------------------------------------------------

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

    X_train = normal_train[FEATURES]
    X_test = test[FEATURES]
    y_test = test["label"]

    print("\nEvaluation dataset:")
    print(f"Training normal : {len(X_train)}")
    print(f"Test normal     : {len(normal_test)}")
    print(f"Test anomalies  : {len(anomalies)}")
    print(f"Total test      : {len(test)}")

    # ---------------------------------------------------------
    # Models
    # ---------------------------------------------------------

    models = {

        "Isolation Forest": IsolationForest(
            n_estimators=200,
            contamination="auto",
            random_state=42,
            n_jobs=-1,
        ),

        "One-Class SVM": OneClassSVM(
            kernel="rbf",
            gamma="scale",
            nu=0.10,
        ),

        "Local Outlier Factor": LocalOutlierFactor(
            n_neighbors=10,
            contamination=0.10,
            novelty=True,
        ),
    }

    # ---------------------------------------------------------
    # Run comparison
    # ---------------------------------------------------------

    results = []

    for name, model in models.items():

        result = evaluate_model(
            name,
            model,
            X_train,
            X_test,
            y_test,
        )

        results.append(result)

    # ---------------------------------------------------------
    # Results table
    # ---------------------------------------------------------

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "f1",
        ascending=False
    )

    print("\n" + "=" * 70)
    print("FINAL MODEL COMPARISON")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # Save results
    # ---------------------------------------------------------

    output_file = (
        "dataset/processed/"
        "clean_model_comparison.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nComparison saved to: {output_file}"
    )

    # ---------------------------------------------------------
    # Best model
    # ---------------------------------------------------------

    best = results_df.iloc[0]

    print("\n" + "=" * 70)
    print("BEST MODEL")
    print("=" * 70)

    print(f"Model     : {best['model']}")
    print(f"Precision : {best['precision']:.4f}")
    print(f"Recall    : {best['recall']:.4f}")
    print(f"F1 Score  : {best['f1']:.4f}")

    print("\nComparison completed successfully.")


if __name__ == "__main__":
    main()
