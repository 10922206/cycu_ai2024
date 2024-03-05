import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 抓取網頁內容
url1 = "https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx"
url2 = "https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil2019.aspx"
response1 = requests.get(url1)
response2 = requests.get(url2)

# 解析網頁內容
soup1 = BeautifulSoup(response1.text, 'html.parser')
soup2 = BeautifulSoup(response2.text, 'html.parser')

# 找到所有的 table 標籤
tables1 = soup1.find_all('table')
tables2 = soup2.find_all('table')

# 將 HTML 表格轉換為 DataFrame
df1 = pd.read_html(str(tables1[1]))[0]
print(df1)
df2 = pd.read_html(str(tables2[1]))[0]
print(df2)
# 將 Dataframe 輸出到 CSV
df1.to_csv('oil1.csv', index=False, encoding='utf-8-sig')
df2.to_csv('oil2.csv', index=False, encoding='utf-8-sig')

# 只保留前五個欄位資料
df1 = df1.iloc[:, :5]
df2 = df2.iloc[:, :5]

# 去除包含 NaN 值的行
df1 = df1.dropna()
df2 = df2.dropna()

# 或者填充 NaN 值
df1 = df1.fillna(0)
df2 = df2.fillna(0)



# 繪製折線圖
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))

# 繪製折線
plt.plot(df1[df1.columns[0]], df1[df1.columns[1]], label=df1.columns[1], color='red')
plt.plot(df1[df1.columns[0]], df1[df1.columns[2]], label=df1.columns[2], color='blue')
plt.plot(df1[df1.columns[0]], df1[df1.columns[3]], label=df1.columns[3], color='green')
plt.plot(df1[df1.columns[0]], df1[df1.columns[4]], label=df1.columns[4], color='purple')

plt.plot(df2[df2.columns[0]], df2[df2.columns[1]], color='red')
plt.plot(df2[df2.columns[0]], df2[df2.columns[2]], color='blue')
plt.plot(df2[df2.columns[0]], df2[df2.columns[3]], color='green')
plt.plot(df2[df2.columns[0]], df2[df2.columns[4]], color='purple')

plt.xlabel('日期')
plt.ylabel('價格')
plt.title('價格趨勢圖')
plt.legend()  # 顯示圖例

# 翻轉 x 軸的座標
plt.gca().invert_xaxis()

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定中文字型為微軟正黑體

plt.show()
print("指令執行完成")
