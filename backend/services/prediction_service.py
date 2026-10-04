import time

from monitoring.metrics import collect_metrics
from ml.predict import predict
from backend.database.database import save_prediction


def get_live_prediction():
    """
    Collect two Linux metric snapshots,
    generate a real-time ML prediction,
    and save the result to SQLite.
    """

    previous_metrics = collect_metrics()

    time.sleep(5)

    current_metrics = collect_metrics()

    result = predict(
        previous_metrics,
        current_metrics,
        5
    )

    save_prediction(result)

    return result
