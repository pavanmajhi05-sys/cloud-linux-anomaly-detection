import csv
import os

CPU_FILE = "dataset/processed/cpu_experiment_labeled.csv"
DISK_FILE = "dataset/processed/disk_io_experiment_labeled.csv"

OUTPUT_FILE = "dataset/processed/clean_combined_anomaly_dataset.csv"


FIELDS = [
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


def read_csv(filename):
    with open(filename, "r", newline="") as file:
        return list(csv.DictReader(file))


def calculate_rates(rows):
    """
    Calculate network and disk I/O rates from cumulative counters.
    """

    previous = None

    for row in rows:

        if previous is None:
            row["network_in_rate"] = 0.0
            row["network_out_rate"] = 0.0
            row["disk_read_rate"] = 0.0
            row["disk_write_rate"] = 0.0

            previous = row
            continue

        from datetime import datetime

        current_time = datetime.strptime(
            row["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        previous_time = datetime.strptime(
            previous["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        delta = (
            current_time - previous_time
        ).total_seconds()

        if delta <= 0:
            delta = 1

        # Network rates
        network_in_rate = (
            float(row["network_in"])
            - float(previous["network_in"])
        ) / delta

        network_out_rate = (
            float(row["network_out"])
            - float(previous["network_out"])
        ) / delta

        # Disk rates
        disk_read_rate = (
            float(row["disk_read_bytes"])
            - float(previous["disk_read_bytes"])
        ) / delta

        disk_write_rate = (
            float(row["disk_write_bytes"])
            - float(previous["disk_write_bytes"])
        ) / delta

        # Protect against counter resets
        row["network_in_rate"] = max(
            network_in_rate, 0.0
        )

        row["network_out_rate"] = max(
            network_out_rate, 0.0
        )

        row["disk_read_rate"] = max(
            disk_read_rate, 0.0
        )

        row["disk_write_rate"] = max(
            disk_write_rate, 0.0
        )

        previous = row


def convert_cpu_rows(rows):
    """
    Convert CPU experiment rows into the common format.
    """

    calculate_rates(rows)

    output = []

    for row in rows:

        output.append({
            "timestamp": row["timestamp"],
            "cpu": row["cpu"],
            "memory": row["memory"],
            "disk": row["disk"],
            "network_in_rate": row["network_in_rate"],
            "network_out_rate": row["network_out_rate"],
            "disk_read_rate": row["disk_read_rate"],
            "disk_write_rate": row["disk_write_rate"],
            "load": row["load"],
            "process_count": row["process_count"],
            "label": row["label"],
            "anomaly_type": row["anomaly_type"],
        })

    return output


def convert_disk_rows(rows):
    """
    Convert disk experiment rows into the common format.
    """

    output = []

    for row in rows:

        output.append({
            "timestamp": row["timestamp"],
            "cpu": row["cpu"],
            "memory": row["memory"],
            "disk": row["disk"],
            "network_in_rate": row["network_in_rate"],
            "network_out_rate": row["network_out_rate"],
            "disk_read_rate": row["disk_read_rate"],
            "disk_write_rate": row["disk_write_rate"],
            "load": row["load"],
            "process_count": row["process_count"],
            "label": row["label"],
            "anomaly_type": row["anomaly_type"],
        })

    return output


def main():

    print("=" * 70)
    print("CREATING CLEAN CPU + DISK-I/O DATASET")
    print("=" * 70)

    print("\nLoading CPU dataset...")
    cpu_rows = read_csv(CPU_FILE)

    print(f"CPU samples: {len(cpu_rows)}")

    print("\nLoading disk-I/O dataset...")
    disk_rows = read_csv(DISK_FILE)

    print(f"Disk-I/O samples: {len(disk_rows)}")

    print("\nProcessing CPU dataset...")
    cpu_data = convert_cpu_rows(cpu_rows)

    print("Processing disk-I/O dataset...")
    disk_data = convert_disk_rows(disk_rows)

    combined = cpu_data + disk_data

    # Sort chronologically
    combined.sort(
        key=lambda row: row["timestamp"]
    )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )

        writer.writeheader()
        writer.writerows(combined)

    # Statistics
    total = len(combined)

    normal = sum(
        row["label"] == "0"
        for row in combined
    )

    cpu_anomalies = sum(
        row["anomaly_type"] == "cpu_anomaly"
        for row in combined
    )

    disk_anomalies = sum(
        row["anomaly_type"] == "disk_io_anomaly"
        for row in combined
    )

    print("\n" + "=" * 70)
    print("CLEAN COMBINED DATASET CREATED")
    print("=" * 70)

    print(f"Total samples       : {total}")
    print(f"Normal samples      : {normal}")
    print(f"CPU anomalies       : {cpu_anomalies}")
    print(f"Disk-I/O anomalies  : {disk_anomalies}")

    print(f"\nOutput file:")
    print(OUTPUT_FILE)

    print("=" * 70)


if __name__ == "__main__":
    main()
