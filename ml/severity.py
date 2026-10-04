def calculate_severity(anomaly_score):
    """
    Convert Isolation Forest anomaly score into a severity level.

    Lower scores indicate stronger anomalies.
    """

    if anomaly_score >= -0.05:
        return "LOW"

    elif anomaly_score >= -0.15:
        return "MEDIUM"

    else:
        return "HIGH"
