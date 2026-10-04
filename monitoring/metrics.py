import psutil
import time

def collect_metrics():
    """Collect a single snapshot of system metrics."""
    net = psutil.net_io_counters()
    
    metrics = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "network_in": net.bytes_recv,
        "network_out": net.bytes_sent,
        "load": psutil.getloadavg()[0],
        "process_count": len(psutil.pids()),
    }
    return metrics
