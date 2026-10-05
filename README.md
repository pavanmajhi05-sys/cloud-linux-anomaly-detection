
# Cloud Linux AI Monitor

Machine Learning-Based Anomaly Detection for Cloud-Based Linux Server Resource Monitoring.

This TRW project monitors Linux server resources, detects abnormal system behavior using Machine Learning, stores monitoring history, exposes REST APIs, and displays the results through a React dashboard.

---

## Project Objective

The goal of this project is to detect abnormal behavior on Linux servers using system resource metrics such as:

- CPU usage
- Memory usage
- Disk usage
- Network traffic
- Disk I/O
- Load average
- Process count

The system uses an Isolation Forest machine-learning model to identify unusual resource behavior.

---

## Architecture

```text
RHEL Linux Server
       |
       v
Python Monitoring / psutil
       |
       v
Feature Engineering
       |
       v
Isolation Forest ML Model
       |
       v
Anomaly Score + Severity
       |
       v
SQLite Database
       |
       v
FastAPI REST API
       |
       v
React + Recharts Dashboard
