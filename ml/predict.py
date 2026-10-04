import pandas as pd
import os
import sys
import time
import joblib

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from monitoring.metrics import collect_metrics
from ml.severity import calculate_severity


MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "ml",
    "model",
    "isolation_forest_clean.joblib"
)


def calculate_rates(previous, current, elapsed_seconds):
    """
    Calculate per-second network and disk I/O rates
    from cumulative system counters.
    """

    if elapsed_seconds <= 0:
        raise ValueError("Elapsed time must be greater than zero.")

    return {
        "network_in_rate": (
            current["network_in"] - previous["network_in"]
        ) / elapsed_seconds,

        "network_out_rate": (
            current["network_out"] - previous["network_out"]
        ) / elapsed_seconds,

        "disk_read_rate": (
            current["disk_read_bytes"] - previous["disk_read_bytes"]
        ) / elapsed_seconds,

        "disk_write_rate": (
            current["disk_write_bytes"] - previous["disk_write_bytes"]
        ) / elapsed_seconds,
    }


def prepare_features(metrics, rates):
    """
    Prepare features in exactly the same order
    used during model training.
    """

    return pd.DataFrame([{
    "cpu": metrics["cpu"],
    "memory": metrics["memory"],
    "disk": metrics["disk"],
    "network_in_rate": rates["network_in_rate"],
    "network_out_rate": rates["network_out_rate"],
    "disk_read_rate": rates["disk_read_rate"],
    "disk_write_rate": rates["disk_write_rate"],
    "load": metrics["load"],
    "process_count": metrics["process_count"],
}])


def load_model():
    """Load the trained Isolation Forest model."""
    return joblib.load(MODEL_PATH)


def predict(previous_metrics, current_metrics, elapsed_seconds):
    """
    Run anomaly prediction using two metric snapshots.
    """

    model = load_model()

    rates = calculate_rates(
        previous_metrics,
        current_metrics,
        elapsed_seconds
    )

    features = prepare_features(current_metrics, rates)

    prediction = model.predict(features)[0]
    anomaly_score = model.decision_function(features)[0]

    status = "NORMAL" if prediction == 1 else "ANOMALY"

    severity = (
        "NONE"
        if status == "NORMAL"
        else calculate_severity(anomaly_score)
    )

    return {
        "timestamp": current_metrics["timestamp"],
        "status": status,
        "anomaly_score": round(float(anomaly_score), 4),
        "severity": severity,

        "cpu": current_metrics["cpu"],
        "memory": current_metrics["memory"],
        "disk": current_metrics["disk"],

        "network_in_rate": round(rates["network_in_rate"], 2),
        "network_out_rate": round(rates["network_out_rate"], 2),
        "disk_read_rate": round(rates["disk_read_rate"], 2),
        "disk_write_rate": round(rates["disk_write_rate"], 2),

        "load": current_metrics["load"],
        "process_count": current_metrics["process_count"],
    }


if __name__ == "__main__":

    print("Collecting first metric snapshot...")
    previous_metrics = collect_metrics()

    print("Waiting 5 seconds for the second snapshot...")
    time.sleep(5)

    print("Collecting second metric snapshot...")
    current_metrics = collect_metrics()

    result = predict(
        previous_metrics,
        current_metrics,
        5
    )

    print("\n===== CLOUD LINUX AI MONITOR =====")
    print(f"Timestamp      : {result['timestamp']}")
    print(f"Status         : {result['status']}")
    print(f"Anomaly Score  : {result['anomaly_score']}")
    print(f"Severity       : {result['severity']}")
    print(f"CPU            : {result['cpu']}%")
    print(f"Memory         : {result['memory']}%")
    print(f"Disk           : {result['disk']}%")
    print(f"Network In     : {result['network_in_rate']} bytes/sec")
    print(f"Network Out    : {result['network_out_rate']} bytes/sec")
    print(f"Disk Read      : {result['disk_read_rate']} bytes/sec")
    print(f"Disk Write     : {result['disk_write_rate']} bytes/sec")
    print(f"Load           : {result['load']}")
    print(f"Processes      : {result['process_count']}")
    print("=================================\n")
