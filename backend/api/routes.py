from fastapi import APIRouter
import sqlite3

from backend.services.prediction_service import get_live_prediction
from backend.database.database import DATABASE_PATH


router = APIRouter(prefix="/api", tags=["Monitoring"])


@router.get("/prediction")
def get_prediction():
    """Generate and return a live ML prediction."""

    return get_live_prediction()


@router.get("/metrics/history")
def get_metrics_history(limit: int = 20):
    """Return recent monitoring records from SQLite."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            status,
            anomaly_score,
            severity,
            cpu,
            memory,
            disk,
            network_in_rate,
            network_out_rate,
            disk_read_rate,
            disk_write_rate,
            load,
            process_count
        FROM monitoring_results
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return {
        "count": len(rows),
        "data": [dict(row) for row in rows]
    }
