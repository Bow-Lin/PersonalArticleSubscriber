# PersonalArticleSubscriber

## 功能(中文版)

- 订阅个人博客文章
- 定期检查博客是否有新文章
- 将新文章推送到微信

## Function(English)

- Subscribe to personal blog articles
- Check for new articles on the blog regularly
- Push new articles to WeChat

## 使用方法

1. 安装依赖
    ```bash
    pip install -r requirements.txt
    ``` 
2. 配置config.yaml
    ```yaml
    website_url: "https://lilianweng.github.io/"
    interval_minutes: 60
    ```
3. 运行doc-tracker.py
    ```bash
    python doc-tracker.py
    ```

## 依赖

- requests
- beautifulsoup4
- schedule
- PyYAML
