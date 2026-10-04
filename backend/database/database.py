import sqlite3
import os


# Project root directory
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATABASE_DIR = os.path.join(PROJECT_ROOT, "backend", "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "monitor.db")


def get_connection():
    """Create and return a SQLite database connection."""

    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the monitoring table if it doesn't exist."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            anomaly_score REAL NOT NULL,
            severity TEXT NOT NULL,
            cpu REAL NOT NULL,
            memory REAL NOT NULL,
            disk REAL NOT NULL,
            network_in_rate REAL NOT NULL,
            network_out_rate REAL NOT NULL,
            disk_read_rate REAL NOT NULL,
            disk_write_rate REAL NOT NULL,
            load REAL NOT NULL,
            process_count INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()
def save_prediction(result):
    """Save a prediction result to the database."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO monitoring_results (
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
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        result["timestamp"],
        result["status"],
        result["anomaly_score"],
        result["severity"],
        result["cpu"],
        result["memory"],
        result["disk"],
        result["network_in_rate"],
        result["network_out_rate"],
        result["disk_read_rate"],
        result["disk_write_rate"],
        result["load"],
        result["process_count"],
    ))

    connection.commit()
    connection.close()
