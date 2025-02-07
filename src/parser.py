import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .logger import get_logger

class WebPageParser:
    def __init__(self):
        self.logger = get_logger(__name__)

    def fetch_page(self, url):
        """获取网页内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
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

        for article in soup.select('article'):
            title = article.find('h2')
            link = article.find('a')
            if title and link:
                articles.append({
                    'title': title.text.strip(),
                    'url': link.get('href'),
                    'found_date': datetime.now().isoformat()
                })

        return articles 