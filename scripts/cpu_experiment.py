import sys
import os
import csv
import time

# Add the project root to Python's import path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from monitoring.metrics import collect_metrics


# Output file
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "dataset",
    "snapshots",
    "cpu_experiment.csv"
)

# Collection interval
INTERVAL = 5

# CSV columns
FIELDS = [
    "timestamp",
    "cpu",
    "memory",
    "disk",
    "network_in",
    "network_out",
    "disk_read_bytes",
    "disk_write_bytes",
    "load",
    "process_count",
]


def main():
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Check whether the CSV already exists
    file_exists = os.path.exists(OUTPUT_FILE)

    print("=" * 70)
    print("CLEAN CPU ANOMALY EXPERIMENT COLLECTOR")
    print("=" * 70)
    print(f"Output file : {OUTPUT_FILE}")
    print(f"Interval    : {INTERVAL} seconds")
    print()
    print("Collecting normal system data.")
    print("Press Ctrl+C to stop.")
    print("=" * 70)

    with open(OUTPUT_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        # Write header only for a new file
        if not file_exists:
            writer.writeheader()
            file.flush()

        try:
            while True:
                metrics = collect_metrics()

                # Keep only the fields required by this experiment
                row = {
                    "timestamp": metrics["timestamp"],
                    "cpu": metrics["cpu"],
                    "memory": metrics["memory"],
                    "disk": metrics["disk"],
                    "network_in": metrics["network_in"],
                    "network_out": metrics["network_out"],
                    "disk_read_bytes": metrics["disk_read_bytes"],
                    "disk_write_bytes": metrics["disk_write_bytes"],
                    "load": metrics["load"],
                    "process_count": metrics["process_count"],
                }

                writer.writerow(row)
                file.flush()

                print(
                    f"{row['timestamp']} | "
                    f"CPU: {row['cpu']:5.1f}% | "
                    f"Memory: {row['memory']:5.1f}% | "
                    f"Disk: {row['disk']:5.1f}% | "
                    f"Load: {row['load']:5.2f} | "
                    f"Processes: {row['process_count']}"
                )

                time.sleep(INTERVAL)

        except KeyboardInterrupt:
            print()
            print("=" * 70)
            print("CPU experiment collector stopped.")
            print("=" * 70)


if __name__ == "__main__":
    main()
