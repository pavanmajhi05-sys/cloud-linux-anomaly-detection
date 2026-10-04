import pandas as pd
import os


CPU_FILE = "dataset/processed/labeled_metrics.csv"
DISK_FILE = "dataset/processed/disk_io_labeled.csv"
OUTPUT_FILE = "dataset/processed/combined_anomaly_dataset.csv"


print("=" * 70)
print("COMBINING CPU AND DISK-I/O EXPERIMENTS")
print("=" * 70)


# --------------------------------------------------
# 1. Load CPU experiment
# --------------------------------------------------

print("\nLoading CPU experiment...")

cpu_df = pd.read_csv(CPU_FILE)

print(f"CPU samples: {len(cpu_df)}")

cpu_df["timestamp"] = pd.to_datetime(cpu_df["timestamp"])


# --------------------------------------------------
# 2. Calculate CPU experiment network rates
# --------------------------------------------------

cpu_df["time_diff"] = (
    cpu_df["timestamp"]
    .diff()
    .dt.total_seconds()
)

network_in_delta = (
    cpu_df["network_in"]
    .diff()
    .fillna(0)
    .clip(lower=0)
)

network_out_delta = (
    cpu_df["network_out"]
    .diff()
    .fillna(0)
    .clip(lower=0)
)

time_diff = cpu_df["time_diff"].replace(0, pd.NA)

cpu_df["network_in_rate"] = (
    network_in_delta / time_diff
).fillna(0)

cpu_df["network_out_rate"] = (
    network_out_delta / time_diff
).fillna(0)


# --------------------------------------------------
# 3. Add disk-I/O features to CPU experiment
# --------------------------------------------------

cpu_df["disk_read_rate"] = 0.0
cpu_df["disk_write_rate"] = 0.0


# --------------------------------------------------
# 4. Identify CPU anomalies
# --------------------------------------------------

cpu_anomaly_timestamps = [
    "2026-10-04 09:20:56",
    "2026-10-04 09:21:07",
    "2026-10-04 09:21:18",
    "2026-10-04 09:21:29",
    "2026-10-04 09:21:40",
    "2026-10-04 09:21:51",
]

cpu_df["anomaly_type"] = "normal"

cpu_df.loc[
    cpu_df["timestamp"].isin(
        pd.to_datetime(cpu_anomaly_timestamps)
    ),
    "anomaly_type"
] = "cpu_anomaly"


# --------------------------------------------------
# 5. Load disk-I/O experiment
# --------------------------------------------------

print("\nLoading disk-I/O experiment...")

disk_df = pd.read_csv(DISK_FILE)

print(f"Disk-I/O samples: {len(disk_df)}")

disk_df["timestamp"] = pd.to_datetime(
    disk_df["timestamp"]
)


# --------------------------------------------------
# 6. Add disk anomaly type
# --------------------------------------------------

disk_df["anomaly_type"] = "normal"

disk_df.loc[
    disk_df["label"] == 1,
    "anomaly_type"
] = "disk_io_anomaly"


# --------------------------------------------------
# 7. Select common columns
# --------------------------------------------------

columns = [
    "timestamp",
    "cpu",
    "memory",
    "disk",
    "network_in_rate",
    "network_out_rate",
    "disk_read_rate",
    "disk_write_rate",
    "load",
    "process_count",
    "label",
    "anomaly_type",
]

cpu_df = cpu_df[columns]
disk_df = disk_df[columns]


# --------------------------------------------------
# 8. Combine datasets
# --------------------------------------------------

combined_df = pd.concat(
    [cpu_df, disk_df],
    ignore_index=True
)


# --------------------------------------------------
# 9. Sort chronologically
# --------------------------------------------------

combined_df = combined_df.sort_values(
    "timestamp"
).reset_index(drop=True)


# --------------------------------------------------
# 10. Save combined dataset
# --------------------------------------------------

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

combined_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 11. Summary
# --------------------------------------------------

print("\n" + "=" * 70)
print("COMBINED DATASET SUMMARY")
print("=" * 70)

print(f"\nTotal samples: {len(combined_df)}")

print("\nAnomaly type distribution:")
print(
    combined_df["anomaly_type"]
    .value_counts()
)

print("\nLabel distribution:")
print(
    combined_df["label"]
    .value_counts()
)

print("\nKnown anomaly samples:")

print(
    combined_df[
        combined_df["label"] == 1
    ][
        [
            "timestamp",
            "cpu",
            "disk",
            "disk_write_rate",
            "label",
            "anomaly_type",
        ]
    ].to_string(index=False)
)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\nCombined dataset created successfully.")
