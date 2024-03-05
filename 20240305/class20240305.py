import requests
from bs4 import BeautifulSoup
import pandas as pd

# 抓取網頁內容
url = "https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx"
response = requests.get(url)

# 解析網頁內容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的 table 標籤
tables = soup.find_all('table')

# 將 HTML 表格轉換為 DataFrame
df1 = pd.read_html(str(tables[0]))[0]
df2 = pd.read_html(str(tables[1]))[0]

print(df1)
print(df2)

#將Dataframe 輸出到 CSV
df2.to_csv('oil.csv', index=False, encoding='utf-8-sig')

#df2 只保留前五個欄位資料
df2 = df2.iloc[:, :5]


# 去除包含 NaN 值的行
df2 = df2.dropna()

# 或者填充 NaN 值
df2 = df2.fillna(0)

# 繪製折線圖
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))

# 繪製折線
plt.plot(df2[df2.columns[0]], df2[df2.columns[1]], label=df2.columns[1])
plt.plot(df2[df2.columns[0]], df2[df2.columns[2]], label=df2.columns[2])
plt.plot(df2[df2.columns[0]], df2[df2.columns[3]], label=df2.columns[3])
plt.plot(df2[df2.columns[0]], df2[df2.columns[4]], label=df2.columns[4])

plt.xlabel('日期')
plt.ylabel('價格')
plt.title('價格趨勢圖')
plt.legend()  # 顯示圖例

# 翻轉 x 軸的座標
plt.gca().invert_xaxis()

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定中文字型為微軟正黑體

plt.show()
