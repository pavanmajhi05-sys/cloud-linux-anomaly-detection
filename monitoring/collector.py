import time
from metrics import collect_metrics
from logger import log_metrics

INTERVAL_SECONDS = 10

def run():
    print("Starting metric collection... (Ctrl+C to stop)")
    while True:
        data = collect_metrics()
        log_metrics(data)
        print(data)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run()
