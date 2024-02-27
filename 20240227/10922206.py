print("Hello, World!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

import csv
import requests
from bs4 import BeautifulSoup
import os

# 打印當前工作目錄
print("當前工作目錄:", os.getcwd())

# 發送 GET 請求
response = requests.get('https://news.pts.org.tw/xml/newsfeed.xml')

# 解析 XML 數據
soup = BeautifulSoup(response.content, 'xml')

# 找到所有的 <title> 標籤
titles = soup.find_all('title')

# 打開 CSV 檔案進行寫入
with open('news_titles_and_summaries.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['標題', '摘要'])  # 寫入 CSV 檔案的標題行

    # 將標題和摘要寫入 CSV 檔案
    for title in titles:
        title_text = title.text.strip()
        summary_text = title.find_next('summary').text.strip()
        writer.writerow([title_text, summary_text])

print("CSV 檔案已成功寫入到指定路徑")
