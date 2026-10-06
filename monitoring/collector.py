import os
import sys
import time

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from monitoring.metrics import collect_metrics
from monitoring.logger import log_metrics


INTERVAL_SECONDS = 10


def run():
    print("Starting Cloud Linux monitoring agent...")
    print(f"Collection interval: {INTERVAL_SECONDS} seconds")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            data = collect_metrics()
            log_metrics(data)

            print(
                f"[{data['timestamp']}] "
                f"CPU={data['cpu']}% "
                f"Memory={data['memory']}% "
                f"Disk={data['disk']}% "
                f"Load={data['load']}"
            )

            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nMonitoring agent stopped.")


if __name__ == "__main__":
    run()
