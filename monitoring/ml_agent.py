import os
import sys
import time

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from monitoring.metrics import collect_metrics
from ml.predict import predict
from backend.database.database import initialize_database, save_prediction


INTERVAL_SECONDS = 10


def run():
    print("Starting Cloud Linux AI monitoring agent...")
    print(f"Prediction interval: {INTERVAL_SECONDS} seconds")
    print("Press Ctrl+C to stop.")

    initialize_database()

    print("\nCollecting initial metric snapshot...")
    previous_metrics = collect_metrics()

    try:
        while True:
            time.sleep(INTERVAL_SECONDS)

            current_metrics = collect_metrics()

            result = predict(
                previous_metrics,
                current_metrics,
                INTERVAL_SECONDS
            )

            save_prediction(result)

            print(
                f"[{result['timestamp']}] "
                f"Status={result['status']} "
                f"Severity={result['severity']} "
                f"Score={result['anomaly_score']} "
                f"CPU={result['cpu']}% "
                f"Memory={result['memory']}%"
            )

            previous_metrics = current_metrics

    except KeyboardInterrupt:
        print("\nCloud Linux AI monitoring agent stopped.")


if __name__ == "__main__":
    run()
