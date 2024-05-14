import pandas as pd



# 讀取 CSV 文件，指定 'big5' 編碼
df2 = pd.read_csv('M05A_20240429.csv', encoding='big5')


df2 = df2[df2['GantryFrom'].str.startswith('01F')]
# 將 'TimeInterval' 列轉換為 datetime 對象
df2['TimeInterval'] = pd.to_datetime(df2['TimeInterval'])

# 計算從開始日期和時間開始的分鐘數
start_time = df2['TimeInterval'].min()

df2['TimeInterval'] = df2['TimeInterval'].apply(lambda x: int((x - start_time).total_seconds() / (5 * 60)) + 1)

df2['GantryID'] = df2['GantryFrom'].apply(lambda x: x[3:7] if len(x) >= 7 and x[:3] == '01F' else x)



# 在 df2 中加入 'direction' 列
df2['direction'] = df2['GantryFrom'].apply(lambda x: 0 if 'N' in x else 1)

print(df2.head())

# 合併 df1 和 df2
df = pd.merge( df2, on=['TimeInterval', 'GantryID', 'direction', 'VehicleType'], how='inner')

# 刪除 df2 的 '交通量' 列
df = df.drop(columns=['交通量_y'])

# 重新命名 df1 的 '交通量' 列
df = df.rename(columns={'交通量_x': '交通量'})

# 合併 df1 和 df2
df = pd.merge(df2, on=['TimeInterval', 'GantryID', 'direction', 'VehicleType'], how='inner')

# 刪除 df2 的 '交通量' 列
df = df.drop(columns=['交通量_y'])

# 重新命名 df1 的 '交通量' 列
df = df.rename(columns={'交通量_x': '交通量'})

#小客車=VehicleType=31
#加入列'小客車'
df['小客車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 31 else 0, axis=1)
df['小貨車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 32 else 0, axis=1)
df['大客車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 41 else 0, axis=1)
df['大貨車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 42 else 0, axis=1)
df['聯結車'] = df.apply(lambda row: row['交通量'] if row['VehicleType'] == 5 else 0, axis=1)

#加入新的列'小客車交通量'
#小客車交通量=VehicleType=31=交通量
df['小客車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 31 else 0, axis=1)
df['小貨車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 32 else 0, axis=1)
df['大客車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 41 else 0, axis=1)
df['大貨車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 42 else 0, axis=1)
df['聯結車速度'] = df.apply(lambda row: row['SpaceMeanSpeed'] if row['VehicleType'] == 5 else 0, axis=1)

#GantryID 改為數字 例如:0005=5 0010=10
df['GantryID'] = df['GantryID'].apply(lambda x: int(x) if x.isdigit() else x)

# 'TimeInterval', 'GantryID','direction' 相同者合併成
#TimeInterval GantryID  小客車  小貨車  大客車  大貨車  聯結車  direction  小客車速度  小貨車速度  大客車速度  大貨車速度  聯結車速度
#0             1        2   24    5    2    0    0          1     90      90      0      0      0
df = df.groupby(['TimeInterval', 'GantryID', 'direction']).sum().reset_index()

# 只保留 'TimeInterval', 'GantryID', 'VehicleType', '交通量', 'direction', 和 'SpaceMeanSpeed' 這幾列
df = df[['TimeInterval', 'GantryID', '小客車', '小貨車', '大客車', '大貨車', '聯結車', 'direction','小客車速度', '小貨車速度', '大客車速度', '大貨車速度', '聯結車速度']]



# 將合併後的 DataFrame 寫入新的 CSV 文件
df.to_csv('Total.csv', index=False, encoding='big5')

# 顯示 DataFrame 的前五行
print(df.head())

#幫我畫一張圖
#x軸是TimeInterval
#y軸是GantryID
#z軸是小客車速度
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_color(speed):
    if speed <= 20:
        return 'purple'
    elif speed <= 40:
        return 'red'
    elif speed <= 60:
        return 'orange'
    elif speed <= 80:
        return 'yellow'
    else:
        return 'green'

df['color'] = df['小客車速度'].apply(get_color)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['TimeInterval'], df['GantryID'], df['小客車速度'], c=df['color'])
ax.set_xlabel('TimeInterval')
ax.set_ylabel('GantryID')
ax.set_zlabel('小客車速度')

plt.show()

