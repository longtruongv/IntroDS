# Requirement:
- Có Docker, Docker Compose
- Tải MongoDB Compass về để xem database

# Chạy Demo:
1. Chạy MongoDB:
- cd mongodb
- docker compose up
- vào MongoDB Compass kết nối vào URI: mongodb://localhost:27017
2. Chạy crawler (mở terminal mới):
- cd news_crawler
- scrapy crawl baomoi

# Cách kết nối
- Config để connect tới server của MongoDB chỉnh trong settings.py
- Thêm MongoDB vào pipelines.py
- Khi đó mỗi khi spider trả về item mới thì sẽ đưa vào pipeline để ghi vào MongoDB 