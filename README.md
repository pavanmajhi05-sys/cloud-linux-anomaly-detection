# Cloud Linux Anomaly Detection (By An AI Agent) :

### Machine Learning-Based Anomaly Detection for Cloud-Based Linux Server Resource Monitoring

Cloud Linux AI Monitor is a machine learning-based Linux server monitoring system designed to detect abnormal system resource utilization using the Isolation Forest algorithm.

The project continuously collects Linux system metrics, analyzes resource behaviour, identifies potential anomalies, and presents monitoring results through a web-based dashboard.

It combines Linux system administration, Python, machine learning, FastAPI, SQLite, and React to provide an integrated server monitoring solution.

---

## 1. Project Overview

Linux servers are essential components of cloud infrastructure. Monitoring CPU, memory, disk, and network utilization is important for maintaining system performance and reliability.

Traditional monitoring systems often depend on manually configured thresholds. This project explores an unsupervised machine learning approach to identify unusual resource behaviour.

The system uses the Isolation Forest algorithm to analyze collected resource metrics and classify observations as normal or anomalous.

### Main Objectives

- Continuously monitor Linux server resource utilization.
- Collect CPU, memory, disk, network, and process metrics.
- Detect abnormal resource behaviour using machine learning.
- Store monitoring results in an SQLite database.
- Provide a web dashboard for monitoring system health.
- Support Linux server administration and troubleshooting.

---

## 2. System Architecture

The project follows this monitoring architecture:

```text
       RHEL Linux Server
              |
              v
      Monitoring Agent
              |
              v
       Metrics Collection
              |
              v
       Feature Processing
              |
              v
       Isolation Forest
              |
              v
       Anomaly Detection
              |
              v
        SQLite Database
              |
              v
          FastAPI
              |
              v
       React Dashboard
              |
              v
       Visual Monitoring
```

---

## 3. Technologies Used

| Category | Technology |
|---|---|
| Operating System | Red Hat Enterprise Linux (RHEL) |
| Programming Language | Python |
| Monitoring | psutil |
| Data Processing | NumPy, Pandas |
| Machine Learning | Scikit-learn |
| Algorithm | Isolation Forest |
| Backend | FastAPI |
| API Server | Uvicorn |
| Database | SQLite |
| Frontend | React.js |
| Build Tool | Vite |
| Visualization | Recharts |
| Version Control | Git and GitHub |
| Service Management | systemd |

---

## 4. Machine Learning Methodology

The project uses the **Isolation Forest** algorithm, an unsupervised machine learning technique for anomaly detection.

Isolation Forest identifies unusual observations by isolating data points through random feature selection and partitioning.

### Monitoring Features

The model uses nine input features:

1. CPU utilization
2. Memory utilization
3. Disk utilization
4. Network input rate
5. Network output rate
6. Disk read rate
7. Disk write rate
8. System load
9. Process count

### Detection Output

The system produces:

- Normal or anomaly status
- Anomaly score
- Severity classification
- Corresponding system resource metrics

Severity levels include LOW, MEDIUM, and HIGH for detected anomalies.

---

## 5. Dataset

The project uses a prepared resource monitoring dataset containing normal and anomalous system observations.

### Dataset Summary

| Category | Samples |
|---|---:|
| Normal | 68 |
| CPU anomalies | 7 |
| Disk I/O anomalies | 4 |
| Total | 79 |

The dataset contains nine numerical monitoring features.

The dataset is used for model training, testing, and performance evaluation.

Dataset file used during model development:

`dataset/processed/clean_combined_anomaly_dataset.csv`

---

## 6. Model Evaluation

The Isolation Forest model was evaluated using a test dataset containing normal observations and labelled anomalies.

### Experimental Results

| Evaluation Metric | Result |
|---|---:|
| Accuracy | 80.00% |
| Precision | 75.00% |
| Recall | 81.82% |
| F1-score | 78.26% |

### Anomaly Detection Results

| Anomaly Type | Detected | Total |
|---|---:|---:|
| CPU anomalies | 5 | 7 |
| Disk I/O anomalies | 4 | 4 |
| Total | 9 | 11 |

The results demonstrate the model's ability to identify abnormal resource behaviour in the prepared dataset.

*Note: These are experimental results from the current dataset and test split. They do not establish production-level detection performance.*

---

## 7. Project Features

### Linux Monitoring

- CPU utilization monitoring
- Memory utilization monitoring
- Disk utilization monitoring
- Network traffic monitoring
- Disk I/O monitoring
- System load monitoring
- Process count monitoring

### Machine Learning

- Unsupervised anomaly detection
- Isolation Forest model
- Anomaly scoring
- Severity classification

### Backend

- FastAPI-based REST API
- SQLite prediction storage
- Latest prediction endpoint
- Historical monitoring records

### Frontend

- React-based monitoring dashboard
- Resource utilization visualization
- Anomaly status display
- Severity information
- Historical metrics charts

### Linux Deployment

- Continuous monitoring using a Python agent
- systemd service integration
- Automatic service restart configuration
- Deployment on RHEL Linux

---

## 8. Project Directory Structure

```text
cloud-linux-anomaly-detection/
│
├── backend/
│   ├── api/
│   │   └── routes.py
│   ├── database/
│   │   └── database.py
│   ├── services/
│   │   └── prediction_service.py
│   └── main.py
│
├── dataset/
│   ├── processed/
│   └── snapshots/
│
├── docs/
│
├── frontend/
│   └── react-dashboard/
│       └── src/
│
├── ml/
│   ├── model/
│   ├── predict.py
│   ├── severity.py
│   └── train.py
│
├── monitoring/
│   ├── collector.py
│   ├── logger.py
│   ├── metrics.py
│   └── ml_agent.py
│
├── notebooks/
├── screenshots/
├── scripts/
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 9. Installation and Setup

### Prerequisites

- RHEL or another compatible Linux distribution
- Python 3.12
- Node.js and npm
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/pavanmajhi05-sys/cloud-linux-anomaly-detection.git

cd cloud-linux-anomaly-detection
```

### Step 2: Create a Python Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the Monitoring Agent

```bash
python monitoring/ml_agent.py
```

The agent collects metrics, generates predictions, and saves results in SQLite.

### Step 5: Start the FastAPI Backend

Open another terminal:

```bash
source .venv/bin/activate

uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

API documentation:

`http://127.0.0.1:8000/docs`

### Step 6: Start the React Dashboard

Open another terminal:

```bash
cd frontend/react-dashboard

npm install

npm run dev
```

Open the dashboard:

`http://localhost:5173`

The backend must be running and accessible to the frontend. The configured CORS origin must match the frontend's actual port.

---

## 10. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend welcome endpoint |
| GET | `/health` | Backend health check |
| GET | `/api/prediction` | Retrieve latest prediction |
| GET | `/api/metrics/history` | Retrieve historical monitoring records |

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

---

## 11. Deployment

The project has been deployed on a RHEL Linux virtual machine.

Deployment directory:

```text
/opt/cloud-linux-anomaly/
├── project/
└── venv/
```

The continuous monitoring agent is managed through systemd.

Service name:

`cloud-linux-monitor.service`

Useful service management commands:

```bash
sudo systemctl status cloud-linux-monitor
```

```bash
sudo systemctl restart cloud-linux-monitor
```

```bash
sudo systemctl enable cloud-linux-monitor
```

View service logs:

```bash
sudo journalctl -u cloud-linux-monitor -f
```

---

## 12. Base Research Paper

**Title:** A Docker Container Anomaly Monitoring System Based on Optimized Isolation Forest

**Publication:** IEEE Transactions on Cloud Computing, 2022.

**DOI:** [10.1109/TCC.2019.2935724](https://doi.org/10.1109/TCC.2019.2935724)

This research provides a related foundation for studying machine learning-based anomaly detection in cloud resource monitoring environments.

Our project adapts the general anomaly detection concept to Linux server resource monitoring using a standard Isolation Forest implementation.

The proposed implementation is not a reproduction of the paper's optimized algorithm.

---

## 13. Future Enhancements

- Additional Linux administrator monitoring features.
- Server process and service monitoring.
- Advanced anomaly analysis.
- Docker container monitoring.
- GitHub Actions for automated testing and CI/CD.
- Additional machine learning model comparisons.
- Improved dataset coverage and model evaluation.
- Extended monitoring and alerting capabilities.

---

## 14. Author

**MAJHI PAVAN**

Master of Computer Applications (MCA)

GitHub: [pavanmajhi05-sys](https://github.com/pavanmajhi05-sys)

Project: Cloud Linux AI Monitor

---

## 15. License

This project is developed for academic and research purposes as part of Technical Research Work (TRW).

