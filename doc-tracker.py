import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import logging
from pathlib import Path
import schedule


class DocumentTracker:
    def __init__(self, url, reading_list_path="reading_list.json", history_path="track_history.json"):
        self.url = url
        self.reading_list_path = Path(reading_list_path)
        self.history_path = Path(history_path)
        self.setup_logging()
        self.initialize_files()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('doc_tracker.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def initialize_files(self):
        # 初始化待阅读列表文件
        if not self.reading_list_path.exists():
            self.save_reading_list([])

        # 初始化历史记录文件
        if not self.history_path.exists():
            self.save_history([])

    def fetch_page(self):
        """获取网页内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logger.error(f"获取页面失败: {str(e)}")
            return None

    def parse_articles(self, html_content):
        """解析网页中的文章链接和标题"""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []

        # 这里的选择器需要根据具体网站结构调整
        for article in soup.select('article'):  # 根据实际网站HTML结构调整选择器
            title = article.find('h2')
            link = article.find('a')
            if title and link:
                articles.append({
                    'title': title.text.strip(),
                    'url': link.get('href'),
                    'found_date': datetime.now().isoformat()
                })

        return articles

    def load_reading_list(self):
        """加载待阅读列表"""
        try:
            with open(self.reading_list_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"加载待阅读列表失败: {str(e)}")
            return []

    def save_reading_list(self, reading_list):
        """保存待阅读列表"""
        with open(self.reading_list_path, 'w', encoding='utf-8') as f:
            json.dump(reading_list, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """加载历史记录"""
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"加载历史记录失败: {str(e)}")
            return []

    def save_history(self, history):
        """保存历史记录"""
        with open(self.history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def check_updates(self):
        """检查网站更新"""
        self.logger.info(f"开始检查更新: {self.url}")

        # 获取网页内容
        html_content = self.fetch_page()
        if not html_content:
            return

        # 解析文章
        current_articles = self.parse_articles(html_content)
        history = self.load_history()
        reading_list = self.load_reading_list()

        # 检查新文章
        history_urls = {item['url'] for item in history}
        new_articles = [
            article for article in current_articles
            if article['url'] not in history_urls
        ]

        if new_articles:
            self.logger.info(f"发现 {len(new_articles)} 篇新文章")

            # 更新历史记录
            history.extend(new_articles)
            self.save_history(history)

            # 更新待阅读列表
            reading_list.extend(new_articles)
            self.save_reading_list(reading_list)

            # 打印新文章信息
            for article in new_articles:
                self.logger.info(f"新文章: {article['title']} - {article['url']}")
        else:
            self.logger.info("没有发现新文章")


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


def load_config(config_path="config.yaml"):
    """Load configuration from a YAML or JSON file"""
    config_path = Path(config_path)
    if config_path.suffix == '.yaml' or config_path.suffix == '.yml':
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif config_path.suffix == '.json':
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise ValueError("Config file must be either YAML or JSON format")


if __name__ == "__main__":
    config = load_config()  # defaults to "config.yaml"
    website_url = config['website_url']
    run_tracker(website_url, interval_minutes=60)
