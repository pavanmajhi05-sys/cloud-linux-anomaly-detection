import csv
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "dataset", "metrics_log.csv")

def log_metrics(metrics):
    """Append one metrics reading to the CSV dataset file."""
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(metrics)
