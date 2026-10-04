import csv
import os

INPUT_FILE = "dataset/snapshots/disk_io_experiment.csv"
OUTPUT_FILE = "dataset/processed/disk_io_experiment_labeled.csv"

DISK_START = "2026-10-04 10:52:47"
DISK_END = "2026-10-04 10:53:05"


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(INPUT_FILE, "r", newline="") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    output_rows = []

    for row in rows:
        timestamp = row["timestamp"].strip()

        # Calculate rates from cumulative counters.
        # The first sample has no previous sample, so rates are 0.
        if len(output_rows) == 0:
            read_rate = 0.0
            write_rate = 0.0
            network_in_rate = 0.0
            network_out_rate = 0.0
        else:
            previous = output_rows[-1]

            # The experiment is sampled approximately every 6 seconds.
            # Use timestamp difference for accurate rate calculation.
            from datetime import datetime

            current_time = datetime.strptime(
                timestamp, "%Y-%m-%d %H:%M:%S"
            )
            previous_time = datetime.strptime(
                previous["timestamp"], "%Y-%m-%d %H:%M:%S"
            )

            delta = (current_time - previous_time).total_seconds()

            if delta <= 0:
                delta = 1

            read_rate = (
                float(row["disk_read_bytes"])
                - float(previous["disk_read_bytes"])
            ) / delta

            write_rate = (
                float(row["disk_write_bytes"])
                - float(previous["disk_write_bytes"])
            ) / delta

            network_in_rate = (
                float(row["network_in"])
                - float(previous["network_in"])
            ) / delta

            network_out_rate = (
                float(row["network_out"])
                - float(previous["network_out"])
            ) / delta

            # Protect against counter resets.
            if read_rate < 0:
                read_rate = 0.0

            if write_rate < 0:
                write_rate = 0.0

            if network_in_rate < 0:
                network_in_rate = 0.0

            if network_out_rate < 0:
                network_out_rate = 0.0

        is_anomaly = DISK_START <= timestamp <= DISK_END

        output_rows.append({
            "timestamp": timestamp,
            "cpu": row["cpu"],
            "memory": row["memory"],
            "disk": row["disk"],
            "network_in": row["network_in"],
            "network_out": row["network_out"],
            "disk_read_bytes": row["disk_read_bytes"],
            "disk_write_bytes": row["disk_write_bytes"],
            "network_in_rate": network_in_rate,
            "network_out_rate": network_out_rate,
            "disk_read_rate": read_rate,
            "disk_write_rate": write_rate,
            "load": row["load"],
            "process_count": row["process_count"],
            "label": 1 if is_anomaly else 0,
            "anomaly_type": "disk_io_anomaly" if is_anomaly else "normal",
        })

    fieldnames = [
        "timestamp",
        "cpu",
        "memory",
        "disk",
        "network_in",
        "network_out",
        "network_in_rate",
        "network_out_rate",
        "disk_read_bytes",
        "disk_write_bytes",
        "disk_read_rate",
        "disk_write_rate",
        "load",
        "process_count",
        "label",
        "anomaly_type",
    ]

    with open(OUTPUT_FILE, "w", newline="") as outfile:
        writer = csv.DictWriter(
            outfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(output_rows)

    anomaly_count = sum(
        row["label"] == 1
        for row in output_rows
    )

    normal_count = len(output_rows) - anomaly_count

    print("=" * 60)
    print("DISK-I/O EXPERIMENT LABELING COMPLETE")
    print("=" * 60)
    print(f"Total samples   : {len(output_rows)}")
    print(f"Normal samples  : {normal_count}")
    print(f"Disk anomalies  : {anomaly_count}")
    print(f"Output file     : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
