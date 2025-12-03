# src/scheduler.py
import time
import logging
from datetime import datetime
from pathlib import Path
from fetch_news import fetch_all_categories
from generate_html import generate

BASE = Path(__file__).resolve().parent.parent
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "scheduler.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# How often to run (in seconds). 600 = 10 minutes
INTERVAL_SECONDS = 10 * 60

def run_cycle():
    logging.info("Starting fetch + generate cycle")
    try:
        fetch_all_categories()   # from src/fetch_news.py
    except Exception as e:
        logging.exception("Error during fetch_all_categories: %s", e)
    try:
        generate(20)             # regenerate 20 latest articles into output/index.html
    except Exception as e:
        logging.exception("Error during generate_html: %s", e)
    logging.info("Cycle finished")

def main_loop():
    logging.info("Scheduler started. Interval = %s seconds", INTERVAL_SECONDS)
    # Run once immediately
    run_cycle()
    # Then run every INTERVAL_SECONDS
    while True:
        time.sleep(INTERVAL_SECONDS)
        run_cycle()

if __name__ == "__main__":
    main_loop()
