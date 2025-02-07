from datetime import datetime
import schedule
import time
from .parser import WebPageParser
from .storage import StorageManager
from .logger import get_logger

class DocumentTracker:
    def __init__(self, url, reading_list_path="reading_list.json", history_path="track_history.json"):
        self.url = url
        self.logger = get_logger(__name__)
        self.parser = WebPageParser()
        self.storage = StorageManager(reading_list_path, history_path)

    def check_updates(self):
        """检查网站更新"""
        self.logger.info(f"开始检查更新: {self.url}")

        # 获取网页内容
        html_content = self.parser.fetch_page(self.url)
        if not html_content:
            return

        # 解析文章
        current_articles = self.parser.parse_articles(html_content)
        history = self.storage.load_history()
        reading_list = self.storage.load_reading_list()

        # 检查新文章
        history_urls = {item['url'] for item in history}
        new_articles = [
            article for article in current_articles
            if article['url'] not in history_urls
        ]

        if new_articles:
            self.logger.info(f"发现 {len(new_articles)} 篇新文章")
            self.storage.update_records(new_articles)
            
            # 打印新文章信息
            for article in new_articles:
                self.logger.info(f"新文章: {article['title']} - {article['url']}")
        else:
            self.logger.info("没有发现新文章") 