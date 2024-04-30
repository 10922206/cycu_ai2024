import pandas as pd

# 讀取 txt 檔案並將其內容轉換為字典
with open('偵測站代號.txt', 'r') as f:
    lines = f.readlines()
gantry_dict = {line.split('=')[0].strip(): int(line.split('=')[1].strip()) for line in lines}

# 讀取 CSV 文件，指定 'big5' 編碼
df1 = pd.read_csv('M03A_20240429.csv', encoding='big5')
df2 = pd.read_csv('M05A_20240429.csv', encoding='big5')

# 將 'TimeInterval' 列轉換為 datetime 對象
df1['TimeInterval'] = pd.to_datetime(df1['TimeInterval'])
df2['TimeInterval'] = pd.to_datetime(df2['TimeInterval'])

# 計算從開始日期和時間開始的分鐘數
start_time = df1['TimeInterval'].min()
df1['TimeInterval'] = df1['TimeInterval'].apply(lambda x: int((x - start_time).total_seconds() / 60) + 1)
df2['TimeInterval'] = df2['TimeInterval'].apply(lambda x: int((x - start_time).total_seconds() / 60) + 1)

# 使用 txt 檔案的內容來轉換 'GantryID' 列
df1['GantryID'] = df1['GantryID'].apply(lambda x: gantry_dict.get(x, x))
df2['GantryID'] = df2['GantryFrom'].apply(lambda x: gantry_dict.get(x, x))

# 將 'direction' 列數據化
df1['direction'] = df1['Direction'].apply(lambda x: 0 if x == 'N' else 1)

# 在 df2 中加入 'direction' 列
df2['direction'] = df2['GantryFrom'].apply(lambda x: 0 if 'N' in x else 1)

# 合併 df1 和 df2
df = pd.merge(df1, df2, on=['TimeInterval', 'GantryID', 'direction', 'VehicleType'], how='inner')

# 刪除 df2 的 '交通量' 列
df = df.drop(columns=['交通量_y'])

# 重新命名 df1 的 '交通量' 列
df = df.rename(columns={'交通量_x': '交通量'})

# 合併 df1 和 df2
df = pd.merge(df1, df2, on=['TimeInterval', 'GantryID', 'direction', 'VehicleType'], how='inner')

# 刪除 df2 的 '交通量' 列
df = df.drop(columns=['交通量_y'])

# 重新命名 df1 的 '交通量' 列
df = df.rename(columns={'交通量_x': '交通量'})

# 只保留 'TimeInterval', 'GantryID', 'VehicleType', '交通量', 'direction', 和 'SpaceMeanSpeed' 這幾列
df = df[['TimeInterval', 'GantryID', 'VehicleType', '交通量', 'direction', 'SpaceMeanSpeed']]

# 將合併後的 DataFrame 寫入新的 CSV 文件
df.to_csv('HW.csv', index=False, encoding='big5')

# 顯示 DataFrame 的前五行
print(df.head())

