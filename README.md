# Cloud Linux Anomaly Monitor

Machine Learning-Based Anomaly Detection for Cloud-Based Linux Server Resource Monitoring — a TRW project combining Linux system administration, Python, machine learning, and full-stack web development.

## Research Question
Can machine-learning techniques detect abnormal behavior in cloud-based Linux servers using system resource metrics?

## Architecture
RHEL Server → Monitoring Agent (psutil) → ML Anomaly Model → FastAPI → React Dashboard

## Project Structure
- `backend/` — FastAPI application
- `frontend/react-dashboard/` — React dashboard
- `monitoring/` — Metric collection agent
- `ml/` — Preprocessing, training, prediction, evaluation
- `scripts/` — Automation (Bash, systemd setup)
- `dataset/` — Collected and public datasets
- `notebooks/` — Experimentation
- `docs/` — TRW documentation, paper drafts
- `screenshots/` — Demo evidence

## Status
🚧 In development — Phase 1 (data collection)

## Author
Majhi Pavan
