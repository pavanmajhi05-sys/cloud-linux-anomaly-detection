import os
import pandas as pd


INPUT_FILE = "dataset/processed/labeled_metrics.csv"
OUTPUT_FILE = "dataset/processed/ml_features.csv"


def preprocess_data():
    print("Loading dataset...")

    df = pd.read_csv(INPUT_FILE)

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Calculate time difference between consecutive samples
    time_diff = df["timestamp"].diff().dt.total_seconds()

    # Calculate network counter differences
    network_in_diff = df["network_in"].diff()
    network_out_diff = df["network_out"].diff()

    # Handle counter resets
    network_in_diff = network_in_diff.where(network_in_diff >= 0, 0)
    network_out_diff = network_out_diff.where(network_out_diff >= 0, 0)

    # Convert cumulative byte counters to bytes per second
    df["network_in_rate"] = network_in_diff / time_diff
    df["network_out_rate"] = network_out_diff / time_diff

    # First sample has no previous measurement
    df["network_in_rate"] = df["network_in_rate"].fillna(0)
    df["network_out_rate"] = df["network_out_rate"].fillna(0)

    # Select ML features
    features = [
        "cpu",
        "memory",
        "disk",
        "network_in_rate",
        "network_out_rate",
        "load",
        "process_count",
    ]

    processed = df[features + ["label"]].copy()

    # Replace any remaining invalid values
    processed = processed.replace([float("inf"), float("-inf")], 0)
    processed = processed.fillna(0)

    # Create output directory if required
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Save processed dataset
    processed.to_csv(OUTPUT_FILE, index=False)

    print("\nPreprocessing completed successfully.")
    print(f"Input samples: {len(df)}")
    print(f"Output samples: {len(processed)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nFeatures:")
    for feature in features:
        print(f" - {feature}")

    print("\nLabel distribution:")
    print(processed["label"].value_counts())


if __name__ == "__main__":
    preprocess_data()
