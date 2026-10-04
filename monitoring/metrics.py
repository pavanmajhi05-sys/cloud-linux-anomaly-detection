import psutil
import time


def collect_metrics():
    """Collect a single snapshot of system metrics."""

    net = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters()

    metrics = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),

        # CPU and memory
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,

        # Filesystem usage
        "disk": psutil.disk_usage("/").percent,

        # Network cumulative counters
        "network_in": net.bytes_recv,
        "network_out": net.bytes_sent,

        # Disk I/O cumulative counters
        "disk_read_bytes": disk_io.read_bytes,
        "disk_write_bytes": disk_io.write_bytes,

        # System load and processes
        "load": psutil.getloadavg()[0],
        "process_count": len(psutil.pids()),
    }

    return metrics
