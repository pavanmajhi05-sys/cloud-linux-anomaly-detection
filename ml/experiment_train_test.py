import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import train_test_split
import joblib
import os


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATASET_PATH = "dataset/processed/ml_features.csv"
MODEL_PATH = "ml/model/isolation_forest_train_test.joblib"

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
# 1. Load dataset
# --------------------------------------------------

print("=" * 60)
print("TRAIN/TEST ANOMALY DETECTION EXPERIMENT")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"Total samples: {len(df)}")

# Separate normal and known anomaly samples
normal_data = df[df["label"] == 0].copy()
anomaly_data = df[df["label"] == 1].copy()

print(f"Normal samples: {len(normal_data)}")
print(f"Known anomaly samples: {len(anomaly_data)}")


# --------------------------------------------------
# 2. Split normal data
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
# 3. Create training and testing datasets
# --------------------------------------------------

# Training contains ONLY normal behavior.
X_train = train_normal[FEATURES]

# Test contains unseen normal samples + known anomalies.
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
# 5. Save separate experiment model
# --------------------------------------------------

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

joblib.dump(model, MODEL_PATH)

print(f"Model saved to: {MODEL_PATH}")


# --------------------------------------------------
# 6. Make predictions
# --------------------------------------------------

print("\nRunning predictions...")

predictions = model.predict(X_test)

# Isolation Forest:
#   1  = normal
#  -1  = anomaly
#
# Convert to:
#   0  = normal
#   1  = anomaly

predicted_labels = (predictions == -1).astype(int)


# --------------------------------------------------
# 7. Calculate metrics
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
# 8. Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("EXPERIMENT RESULTS")
print("=" * 60)

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
        target_names=["Normal", "Anomaly"],
        zero_division=0,
    )
)


# --------------------------------------------------
# 9. False positives / false negatives
# --------------------------------------------------

tn, fp, fn, tp = cm.ravel()

print("=" * 60)
print("ERROR ANALYSIS")
print("=" * 60)

print(f"True Negatives  : {tn}")
print(f"False Positives : {fp}")
print(f"False Negatives : {fn}")
print(f"True Positives  : {tp}")

print("\nExperiment completed successfully.")
print("=" * 60)
