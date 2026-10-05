import { useEffect, useState } from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function MetricCard({ title, value, unit }) {
  return (
    <div className="metric-card">
      <div className="metric-title">{title}</div>

      <div className="metric-value">
        {value}
        <span>{unit}</span>
      </div>
    </div>
  );
}

function App() {
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPrediction = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_URL}/api/prediction`);

      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }

      const data = await response.json();

      setPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch(
        `${API_URL}/api/metrics/history?limit=20`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch history");
      }

      const result = await response.json();

      const formattedData = [...result.data]
        .reverse()
        .map((item) => ({
          ...item,
          time: item.timestamp.substring(11, 19),
        }));

      setHistory(formattedData);
    } catch (err) {
      console.error("History error:", err);
    }
  };

  useEffect(() => {
    fetchPrediction();
    fetchHistory();

    const interval = setInterval(() => {
      fetchPrediction();
      fetchHistory();
    }, 15000);

    return () => clearInterval(interval);
  }, []);

  const isAnomaly = prediction?.status === "ANOMALY";

  return (
    <div className="dashboard">

      {/* HEADER */}
      <header className="dashboard-header">
        <div>
          <h1>Cloud Linux AI Monitor</h1>

          <p>
            Machine Learning Based Linux Server Monitoring
          </p>
        </div>

        <div className="server-status">
          <span className="status-dot"></span>
          SERVER ONLINE
        </div>
      </header>

      {/* LOADING */}
      {loading && !prediction && (
        <div className="message">
          Collecting Linux metrics...
        </div>
      )}

      {/* ERROR */}
      {error && (
        <div className="error-message">
          API Error: {error}
        </div>
      )}

      {prediction && (
        <>
          {/* SYSTEM STATUS */}
          <section className="status-section">

            <div
              className={`status-card ${
                isAnomaly ? "anomaly" : "normal"
              }`}
            >
              <div className="status-label">
                SYSTEM STATUS
              </div>

              <div className="status-value">
                {prediction.status}
              </div>

              <div className="status-score">
                Anomaly Score: {prediction.anomaly_score}
              </div>
            </div>

            <div
              className={`severity-card ${
                prediction.severity.toLowerCase()
              }`}
            >
              <div className="status-label">
                SEVERITY
              </div>

              <div className="status-value">
                {prediction.severity}
              </div>
            </div>

          </section>

          {/* METRIC CARDS */}
          <section className="metrics-grid">

            <MetricCard
              title="CPU"
              value={prediction.cpu}
              unit="%"
            />

            <MetricCard
              title="MEMORY"
              value={prediction.memory}
              unit="%"
            />

            <MetricCard
              title="DISK"
              value={prediction.disk}
              unit="%"
            />

            <MetricCard
              title="LOAD"
              value={prediction.load.toFixed(2)}
              unit=""
            />

            <MetricCard
              title="PROCESSES"
              value={prediction.process_count}
              unit=""
            />

            <MetricCard
              title="NETWORK IN"
              value={prediction.network_in_rate.toFixed(0)}
              unit=" B/s"
            />

            <MetricCard
              title="NETWORK OUT"
              value={prediction.network_out_rate.toFixed(0)}
              unit=" B/s"
            />

            <MetricCard
              title="DISK WRITE"
              value={prediction.disk_write_rate.toFixed(0)}
              unit=" B/s"
            />

          </section>

          {/* CPU CHART */}
          <section className="chart-panel">

            <div className="chart-header">
              <h2>CPU Usage History</h2>
              <span>Last 20 readings</span>
            </div>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <LineChart data={history}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="time" />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="cpu"
                  stroke="#3b82f6"
                  strokeWidth={3}
                  dot={false}
                />

              </LineChart>
            </ResponsiveContainer>

          </section>

          {/* MEMORY CHART */}
          <section className="chart-panel">

            <div className="chart-header">
              <h2>Memory Usage History</h2>
              <span>Last 20 readings</span>
            </div>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <LineChart data={history}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="time" />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="memory"
                  stroke="#8b5cf6"
                  strokeWidth={3}
                  dot={false}
                />

              </LineChart>
            </ResponsiveContainer>

          </section>

          {/* DISK CHART */}
          <section className="chart-panel">

            <div className="chart-header">
              <h2>Disk Usage History</h2>
              <span>Last 20 readings</span>
            </div>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <LineChart data={history}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="time" />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="disk"
                  stroke="#10b981"
                  strokeWidth={3}
                  dot={false}
                />

              </LineChart>
            </ResponsiveContainer>

          </section>

          {/* NETWORK I/O CHART */}
          <section className="chart-panel">

            <div className="chart-header">
              <h2>Network I/O History</h2>
              <span>Last 20 readings</span>
            </div>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <LineChart data={history}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="time" />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="network_in_rate"
                  stroke="#06b6d4"
                  strokeWidth={3}
                  dot={false}
                  name="Network In"
                />

                <Line
                  type="monotone"
                  dataKey="network_out_rate"
                  stroke="#f59e0b"
                  strokeWidth={3}
                  dot={false}
                  name="Network Out"
                />

              </LineChart>
            </ResponsiveContainer>

          </section>

          {/* DISK I/O CHART */}
          <section className="chart-panel">

            <div className="chart-header">
              <h2>Disk I/O History</h2>
              <span>Last 20 readings</span>
            </div>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <LineChart data={history}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="time" />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="disk_read_rate"
                  stroke="#ec4899"
                  strokeWidth={3}
                  dot={false}
                  name="Disk Read"
                />

                <Line
                  type="monotone"
                  dataKey="disk_write_rate"
                  stroke="#f97316"
                  strokeWidth={3}
                  dot={false}
                  name="Disk Write"
                />

              </LineChart>
            </ResponsiveContainer>

          </section>

          {/* INFORMATION */}
          <section className="information-panel">

            <div>
              <h2>Disk Read</h2>

              <p>
                {prediction.disk_read_rate.toFixed(0)} B/s
              </p>
            </div>

            <div>
              <h2>Last Updated</h2>

              <p>
                {prediction.timestamp}
              </p>
            </div>

            <button onClick={fetchPrediction}>
              Refresh Prediction
            </button>

          </section>

        </>
      )}

    </div>
  );
}

export default App;
