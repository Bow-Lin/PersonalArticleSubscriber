import json
from pathlib import Path
from .logger import get_logger

class StorageManager:
    def __init__(self, reading_list_path="reading_list.json", history_path="track_history.json"):
        self.reading_list_path = Path(reading_list_path)
        self.history_path = Path(history_path)
        self.logger = get_logger(__name__)
        self.initialize_files()

    def initialize_files(self):
        if not self.reading_list_path.exists():
            self.save_reading_list([])
        if not self.history_path.exists():
            self.save_history([])

    def load_reading_list(self):
        try:
            with open(self.reading_list_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"加载待阅读列表失败: {str(e)}")
            return []

    def save_reading_list(self, reading_list):
        with open(self.reading_list_path, 'w', encoding='utf-8') as f:
            json.dump(reading_list, f, ensure_ascii=False, indent=2)

    def load_history(self):
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"加载历史记录失败: {str(e)}")
            return []

    def save_history(self, history):
        with open(self.history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def update_records(self, new_articles):
        """Update both history and reading list with new articles"""
        history = self.load_history()
        reading_list = self.load_reading_list()
        
        history.extend(new_articles)
        reading_list.extend(new_articles)
        
        self.save_history(history)
        self.save_reading_list(reading_list) 