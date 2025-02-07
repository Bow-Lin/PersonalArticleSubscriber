import schedule
import time
from src.tracker import DocumentTracker
from src.utils import load_config

def run_tracker(url, interval_minutes=60):
    """运行追踪器"""
    tracker = DocumentTracker(url)

    # 首次运行
    tracker.check_updates()

    # 设置定期检查
    schedule.every(interval_minutes).minutes.do(tracker.check_updates)

    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    config = load_config()  # defaults to "config.yaml"
    website_url = config['website_url']
    run_tracker(website_url, interval_minutes=60) 