import csv
import os

INPUT_FILE = "dataset/snapshots/cpu_experiment.csv"
OUTPUT_FILE = "dataset/processed/cpu_experiment_labeled.csv"

CPU_START = "2026-10-04 11:23:00"
CPU_END = "2026-10-04 11:23:36"


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(INPUT_FILE, "r", newline="") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    anomaly_count = 0

    for row in rows:
        timestamp = row["timestamp"].strip()

        if CPU_START <= timestamp <= CPU_END:
            row["label"] = 1
            row["anomaly_type"] = "cpu_anomaly"
            anomaly_count += 1
        else:
            row["label"] = 0
            row["anomaly_type"] = "normal"

    fieldnames = list(rows[0].keys())

    with open(OUTPUT_FILE, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    normal_count = len(rows) - anomaly_count

    print("=" * 60)
    print("CPU EXPERIMENT LABELING COMPLETE")
    print("=" * 60)
    print(f"Total samples   : {len(rows)}")
    print(f"Normal samples  : {normal_count}")
    print(f"CPU anomalies   : {anomaly_count}")
    print(f"Output file     : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
