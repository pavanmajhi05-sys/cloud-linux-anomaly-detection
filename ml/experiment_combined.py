import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import joblib
import os


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATASET_PATH = "dataset/processed/combined_anomaly_dataset.csv"
MODEL_PATH = "ml/model/isolation_forest_combined.joblib"

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


# --------------------------------------------------
# 1. Load combined dataset
# --------------------------------------------------

print("=" * 70)
print("COMBINED CPU + DISK-I/O ANOMALY EXPERIMENT")
print("=" * 70)

print("\nLoading combined dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"Total samples: {len(df)}")

normal_data = df[df["label"] == 0].copy()
anomaly_data = df[df["label"] == 1].copy()

print(f"Normal samples: {len(normal_data)}")
print(f"Known anomaly samples: {len(anomaly_data)}")

print("\nAnomaly types:")
print(anomaly_data["anomaly_type"].value_counts())


# --------------------------------------------------
# 2. Split ONLY normal data
# --------------------------------------------------

print("\nSplitting normal data...")

train_normal, test_normal = train_test_split(
    normal_data,
    test_size=0.20,
    random_state=42,
    shuffle=True,
)

print(f"Training normal samples: {len(train_normal)}")
print(f"Unseen test normal samples: {len(test_normal)}")


# --------------------------------------------------
# 3. Create train/test sets
# --------------------------------------------------

# Training contains ONLY normal behavior.
X_train = train_normal[FEATURES]

# Testing contains unseen normal behavior + all known anomalies.
test_data = pd.concat(
    [test_normal, anomaly_data],
    ignore_index=True,
)

X_test = test_data[FEATURES]
y_test = test_data["label"]


# --------------------------------------------------
# 4. Train Isolation Forest
# --------------------------------------------------

print("\nTraining Isolation Forest...")

model = IsolationForest(
    n_estimators=200,
    contamination="auto",
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train)

print("Model training completed.")


# --------------------------------------------------
# 5. Save model
# --------------------------------------------------

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True,
)

joblib.dump(
    model,
    MODEL_PATH,
)

print(f"Model saved to: {MODEL_PATH}")


# --------------------------------------------------
# 6. Predict
# --------------------------------------------------

print("\nRunning predictions...")

predictions = model.predict(X_test)

# Isolation Forest:
#  1  = normal
# -1  = anomaly
#
# Convert:
#  0  = normal
#  1  = anomaly

predicted_labels = (
    predictions == -1
).astype(int)


# --------------------------------------------------
# 7. Overall metrics
# --------------------------------------------------

precision = precision_score(
    y_test,
    predicted_labels,
    zero_division=0,
)

recall = recall_score(
    y_test,
    predicted_labels,
    zero_division=0,
)

f1 = f1_score(
    y_test,
    predicted_labels,
    zero_division=0,
)

cm = confusion_matrix(
    y_test,
    predicted_labels,
)


# --------------------------------------------------
# 8. Display overall results
# --------------------------------------------------

print("\n" + "=" * 70)
print("OVERALL EXPERIMENT RESULTS")
print("=" * 70)

print(f"\nTest samples: {len(test_data)}")
print(f"Test normal samples: {len(test_normal)}")
print(f"Test anomaly samples: {len(anomaly_data)}")

print("\nPerformance:")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predicted_labels,
        target_names=[
            "Normal",
            "Anomaly",
        ],
        zero_division=0,
    )
)


# --------------------------------------------------
# 9. Error analysis
# --------------------------------------------------

tn, fp, fn, tp = cm.ravel()

print("=" * 70)
print("ERROR ANALYSIS")
print("=" * 70)

print(f"True Negatives  : {tn}")
print(f"False Positives : {fp}")
print(f"False Negatives : {fn}")
print(f"True Positives  : {tp}")


# --------------------------------------------------
# 10. Analyze each anomaly type
# --------------------------------------------------

print("\n" + "=" * 70)
print("ANOMALY-TYPE ANALYSIS")
print("=" * 70)

results_df = test_data.copy()

results_df["prediction"] = predicted_labels

for anomaly_type in [
    "cpu_anomaly",
    "disk_io_anomaly",
]:

    subset = results_df[
        results_df["anomaly_type"] == anomaly_type
    ]

    actual = subset["label"]
    predicted = subset["prediction"]

    type_precision = precision_score(
        actual,
        predicted,
        zero_division=0,
    )

    type_recall = recall_score(
        actual,
        predicted,
        zero_division=0,
    )

    type_f1 = f1_score(
        actual,
        predicted,
        zero_division=0,
    )

    detected = int(
        (
            (actual == 1)
            & (predicted == 1)
        ).sum()
    )

    missed = int(
        (
            (actual == 1)
            & (predicted == 0)
        ).sum()
    )

    print(f"\n{anomaly_type}:")
    print(f"Samples detected : {detected}")
    print(f"Samples missed   : {missed}")
    print(f"Precision        : {type_precision:.4f}")
    print(f"Recall           : {type_recall:.4f}")
    print(f"F1 Score         : {type_f1:.4f}")


# --------------------------------------------------
# 11. Show detected anomaly samples
# --------------------------------------------------

print("\n" + "=" * 70)
print("KNOWN ANOMALY PREDICTIONS")
print("=" * 70)

known_results = results_df[
    results_df["label"] == 1
][
    [
        "timestamp",
        "anomaly_type",
        "cpu",
        "disk",
        "disk_write_rate",
        "label",
        "prediction",
    ]
]

print(
    known_results.to_string(
        index=False
    )
)


# --------------------------------------------------
# 12. Save experiment results
# --------------------------------------------------

results_output = (
    "dataset/processed/"
    "combined_experiment_results.csv"
)

results_df.to_csv(
    results_output,
    index=False,
)

print(
    f"\nDetailed predictions saved to: "
    f"{results_output}"
)

print("\nCombined experiment completed successfully.")
print("=" * 70)
