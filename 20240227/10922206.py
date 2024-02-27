print("Hello, World!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

import requests
from bs4 import BeautifulSoup

# 發送 GET 請求
response = requests.get('https://news.pts.org.tw/xml/newsfeed.xml')

# 解析 XML 數據
soup = BeautifulSoup(response.content, 'xml')

# 找到所有的 <title> 標籤
titles = soup.find_all('title')

# 打印出所有的標題
for title in titles:
    print(title.text)
    #印出 summary
    print(title.find_next('summary').text)
    print()
    #印出分隔線
    print("=====================================")
    print()
