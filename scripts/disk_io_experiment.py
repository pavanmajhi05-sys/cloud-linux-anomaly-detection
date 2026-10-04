import csv
import os
import time
import psutil


OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "dataset",
    "snapshots",
    "disk_io_experiment.csv"
)

INTERVAL_SECONDS = 5


def collect_metrics():
    net = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters()

    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "network_in": net.bytes_recv,
        "network_out": net.bytes_sent,
        "disk_read_bytes": disk_io.read_bytes,
        "disk_write_bytes": disk_io.write_bytes,
        "load": psutil.getloadavg()[0],
        "process_count": len(psutil.pids()),
    }


def run():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    file_exists = os.path.isfile(OUTPUT_FILE)

    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = None

        if not file_exists:
            writer = csv.DictWriter(
                f,
                fieldnames=[
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
                ],
            )
            writer.writeheader()

        print("Starting disk-I/O experiment collector...")
        print("Collecting every 5 seconds.")
        print("Press Ctrl+C to stop.")

        while True:
            data = collect_metrics()

            if writer is None:
                writer = csv.DictWriter(
                    f,
                    fieldnames=data.keys(),
                )

            writer.writerow(data)
            f.flush()

            print(data)

            time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
