from fastapi import APIRouter
import sqlite3

from backend.database.database import DATABASE_PATH


router = APIRouter(prefix="/api", tags=["Monitoring"])


@router.get("/prediction")
def get_prediction():
    """Return the latest ML prediction stored in SQLite."""

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
        LIMIT 1
    """)

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return {
            "status": "NO_DATA",
            "message": "No monitoring predictions available yet."
        }

    return dict(row)


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
