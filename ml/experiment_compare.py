import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
import joblib
import os


DATASET_PATH = "dataset/processed/ml_features.csv"

FEATURES = [
    "cpu",
    "memory",
    "disk",
    "network_in_rate",
    "network_out_rate",
    "load",
    "process_count",
]


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("=" * 70)
print("ISOLATION FOREST PARAMETER COMPARISON")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

normal_data = df[df["label"] == 0].copy()
anomaly_data = df[df["label"] == 1].copy()

print(f"\nTotal samples: {len(df)}")
print(f"Normal samples: {len(normal_data)}")
print(f"Known anomalies: {len(anomaly_data)}")


# --------------------------------------------------
# Train/Test split
# --------------------------------------------------

train_normal, test_normal = train_test_split(
    normal_data,
    test_size=0.20,
    random_state=42,
    shuffle=True,
)

test_data = pd.concat(
    [test_normal, anomaly_data],
    ignore_index=True,
)

X_train = train_normal[FEATURES]
X_test = test_data[FEATURES]
y_test = test_data["label"]


# --------------------------------------------------
# Models to compare
# --------------------------------------------------

experiments = [
    {
        "name": "IF_100_auto",
        "n_estimators": 100,
        "contamination": "auto",
    },
    {
        "name": "IF_200_auto",
        "n_estimators": 200,
        "contamination": "auto",
    },
    {
        "name": "IF_300_auto",
        "n_estimators": 300,
        "contamination": "auto",
    },
    {
        "name": "IF_200_001",
        "n_estimators": 200,
        "contamination": 0.01,
    },
    {
        "name": "IF_200_002",
        "n_estimators": 200,
        "contamination": 0.02,
    },
    {
        "name": "IF_200_003",
        "n_estimators": 200,
        "contamination": 0.03,
    },
]


results = []


# --------------------------------------------------
# Run experiments
# --------------------------------------------------

for config in experiments:

    print(f"\nRunning: {config['name']}")

    model = IsolationForest(
        n_estimators=config["n_estimators"],
        contamination=config["contamination"],
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train)

    predictions = model.predict(X_test)

    predicted_labels = (predictions == -1).astype(int)

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

    false_positives = (
        ((y_test == 0) & (predicted_labels == 1))
        .sum()
    )

    false_negatives = (
        ((y_test == 1) & (predicted_labels == 0))
        .sum()
    )

    results.append(
        {
            "Experiment": config["name"],
            "Trees": config["n_estimators"],
            "Contamination": config["contamination"],
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "F1": round(f1, 4),
            "False Positives": int(false_positives),
            "False Negatives": int(false_negatives),
        }
    )


# --------------------------------------------------
# Results table
# --------------------------------------------------

results_df = pd.DataFrame(results)

print("\n")
print("=" * 100)
print("EXPERIMENT COMPARISON")
print("=" * 100)

print(results_df.to_string(index=False))


# --------------------------------------------------
# Select best model
# --------------------------------------------------

best_index = results_df["F1"].idxmax()
best_result = results_df.loc[best_index]

print("\n")
print("=" * 70)
print("BEST CONFIGURATION")
print("=" * 70)

print(f"Experiment       : {best_result['Experiment']}")
print(f"Trees             : {best_result['Trees']}")
print(f"Contamination     : {best_result['Contamination']}")
print(f"Precision         : {best_result['Precision']}")
print(f"Recall            : {best_result['Recall']}")
print(f"F1 Score          : {best_result['F1']}")
print(f"False Positives   : {best_result['False Positives']}")
print(f"False Negatives   : {best_result['False Negatives']}")


# --------------------------------------------------
# Save results
# --------------------------------------------------

output_dir = "dataset/processed"
os.makedirs(output_dir, exist_ok=True)

results_path = os.path.join(
    output_dir,
    "model_comparison.csv",
)

results_df.to_csv(
    results_path,
    index=False,
)

print(f"\nComparison saved to: {results_path}")

print("\nExperiment completed successfully.")
