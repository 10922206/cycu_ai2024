import requests
from bs4 import BeautifulSoup
import pandas as pd

# 使用 for 迴圈生成所有的網址
urls = ['https://www.cwa.gov.tw/rss/forecast/36_{:02d}.xml'.format(i) for i in range(1, 23)]

# 創建一個空的 DataFrame
df = pd.DataFrame(columns=['title', 'description'])

# 定義一個函數來處理每個網址
def process_url(url):
    # 獲取 XML 數據
    response = requests.get(url)

    # 解析 XML 數據
    soup = BeautifulSoup(response.content, 'xml')

    # 找到所有的 'item' 標籤
    items = soup.find_all('item')

    # 對於每個 'item'，找到 'title' 和 'description' 標籤並打印其內容
    for item in items:
        print(url)
        title = item.title.text
        description = item.description.text
        print(title)
        print(description)
        df.loc[len(df)] = [title, description]
    
    # 打印分隔線
    print('-' * 50)

# 遍歷所有的網址並處理
for url in urls:
    process_url(url)