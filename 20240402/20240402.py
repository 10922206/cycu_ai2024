import requests
from bs4 import BeautifulSoup
import pandas as pd

# 使用 for 迴圈生成所有的網址
urls = ['https://www.cwa.gov.tw/rss/forecast/36_{:02d}.xml'.format(i) for i in range(1, 23)]

# 創建一個空的 DataFrame
df = pd.DataFrame(columns=['title', 'description'])

df = pd.DataFrame(columns=['title'])

# 定義一個函數來處理每個網址
def process_url(url):
    # 獲取 XML 數據
    response = requests.get(url)

    # 解析 XML 數據
    soup = BeautifulSoup(response.content, 'xml')

    # 找到所有的 'item' 標籤
    items = soup.find_all('item')


    # 對於每個 'item'，找到 'title' 標籤並打印其內容
    for item in items:
        title = item.title.text 
        df.loc[len(df)] = [title]
        print(title)
        #只需要第一列title
        break

    # 打印分隔線
    print('-' * 50)


#資料格式為( 臺東縣04/02 今晚明晨 晴時多雲 溫度: 24 ~ 27 降雨機率: 10% (04/02 17:00發布))
#將我的title資料分割成縣市名稱、日期、天氣、溫度、降雨機率 
#縣市名稱為前四個字
#日期為第五個字到第十個字
#天氣為第十一個字到第十五個字
#溫度為第十六個字到第二十個字
#降雨機率為第二十一個字到第二十五個字
#建立一個新的DataFrame
df1 = pd.DataFrame(columns=['縣市名稱','日期','天氣','溫度','降雨機率'])
for index, row in df.iterrows():
    title = row['title']
    df1.loc[len(df1)] = [title[:4],title[4:10],title[10:15],title[15:20],title[20:25]]
print(df1)

# 遍歷所有的網址並處理
for url in urls:
    process_url(url)

#尋找台灣的區界地圖 shape file/ geojson file
#read 20240402/tract_20140313.json as geopanas
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

# 讀取 shape file
df_taiwan=gpd.read_file('20240402/county/county_moi_1090820.shp')

# 將 df1 的縣市名稱與 df_taiwan 的 COUNTYNAME 合併
geo_taiwan = pd.merge(df_taiwan, df1, left_on='COUNTYNAME', right_on='縣市名稱')

# 清理數據
geo_taiwan = geo_taiwan.dropna(subset=['geometry'])

# 繪製台灣地圖
geo_taiwan.plot()
plt.xlim(118,122)
plt.ylim(21.5,25.5)

# 繪製台灣地圖，並指定縱橫比
geo_taiwan.plot(aspect=1.0)

# 繪製溫度點
plt.scatter(geo_taiwan['經度'], geo_taiwan['緯度'], c=geo_taiwan['溫度'], cmap='coolwarm')



# 顯示圖形
plt.show()