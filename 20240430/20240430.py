import pandas as pd



# 讀取 CSV 文件，指定 'big5' 編碼
df1 = pd.read_csv('M05A_20240429.csv', encoding='big5')


df1 = df1[df1['GantryFrom'].str.startswith('01F')]
# 將 'TimeInterval' 列轉換為 datetime 對象
df1['TimeInterval'] = pd.to_datetime(df1['TimeInterval'])

# 計算從開始日期和時間開始的分鐘數
start_time = df1['TimeInterval'].min()

df1['TimeInterval'] = df1['TimeInterval'].apply(lambda x: int((x - start_time).total_seconds() / (5 * 60)) + 1)

df1['GantryID'] = df1['GantryFrom'].apply(lambda x: x[3:7] if len(x) >= 7 and x[:3] == '01F' else x)



# 在 df2 中加入 'direction' 列
df1['direction'] = df1['GantryFrom'].apply(lambda x: 0 if 'N' in x else 1)

print(df1.head())

df=df1




#小客車=VehicleType=31
#加入列'小客車'
df['小客車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 31 else 0, axis=1)
df['小貨車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 32 else 0, axis=1)
df['大客車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 41 else 0, axis=1)
df['大貨車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 42 else 0, axis=1)
df['聯結車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 5 else 0, axis=1)
print("完成5%")
#加入新的列'小客車交通量'
#小客車交通量=VehicleType=31=交通量
df['小客車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 31 else 0, axis=1)
df['小貨車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 32 else 0, axis=1)
df['大客車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 41 else 0, axis=1)
df['大貨車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 42 else 0, axis=1)
df['聯結車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 5 else 0, axis=1)
print("完成10%")
#GantryID 改為數字 例如:0005=5 0010=10
df['GantryID'] = df['GantryID'].apply(lambda x: int(x) if x.isdigit() else x)

# 'TimeInterval', 'GantryID','direction' 相同者合併成
#TimeInterval GantryID  小客車  小貨車  大客車  大貨車  聯結車  direction  小客車速度  小貨車速度  大客車速度  大貨車速度  聯結車速度
#0             1        2   24    5    2    0    0          1     90      90      0      0      0
df = df.groupby(['TimeInterval', 'GantryID', 'direction']).sum().reset_index()
print("完成15%")
# 只保留 'TimeInterval', 'GantryID', 'VehicleType', '交通量', 'direction', 和 'SpaceMeanSpeed' 這幾列
df = df[['TimeInterval', 'GantryID', '小客車', '小貨車', '大客車', '大貨車', '聯結車', 'direction','小客車速度', '小貨車速度', '大客車速度', '大貨車速度', '聯結車速度']]

# 將合併後的 Df3df3Frame 寫入新的 CSV 文件
df.to_csv('Total.csv', index=False, encoding='big5')
print("完成50%")
# 顯示 Df3df3Frame 的前五行
print(df.head())

df2 = df.loc[df['direction'] == 1]

#將df2存成新的CSV檔
df2.to_csv('Total2.csv', index=False, encoding='big5')


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
df3 = df2[['TimeInterval', 'GantryID', '小客車']]
print(df3.head())

data = np.array([df2['TimeInterval'], df2['GantryID'].astype(int), df2['小客車']]).T

print (data)
# 創建一個新的圖形 
# 畫出多視角圖形  重 111, 110, 101, 100
# add four subplots to the figure
# subplot(111) is subplot(111,portjection='3d')

# 對時間和里程數據進行網格化
# 假設 x (時間) 和 y (里程) 已經是規則的網格數據
x = np.linspace(data[:, 0].min(), data[:, 0].max(), num=50)  # 調整 num 以匹配數據點的密度
y = np.linspace(data[:, 1].min(), data[:, 1].max(), num=50)
x, y = np.meshgrid(x, y)

# 插值找到每個 (x, y) 點對應的 z (車流量)
from scipy.interpolate import griddata
z = griddata((data[:, 0], data[:, 1]), data[:, 2], (x, y), method='cubic')


fig = plt.figure()



angles = [(30, 135), (30, 45), (30, 225), (30, 315)]
for i, (elev, azim) in enumerate(angles, start=1):
    ax = fig.add_subplot(2, 2, i, projection='3d')
    ax.set_title(f"View {i}")
    surf = ax.plot_surface(x, y, z, cmap='viridis')
    ax.set_xlabel('Time')
    ax.set_ylabel('Mileage')
    ax.set_zlabel('Traffic Volume')
    ax.view_init(elev=elev, azim=azim)
plt.suptitle('10922206')
# Adjust layout
plt.tight_layout()

# Show or save the plot
plt.savefig('cubicspline_4v.png')
plt.show()