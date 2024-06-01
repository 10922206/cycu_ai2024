import pandas as pd

# 讀取CSV檔，使用UTF-8編碼
df = pd.read_csv('20240521/download/M05A_20240101.csv', encoding='utf-8')

# 將 TimeInterval 轉換為 datetime 格式
df['TimeInterval'] = pd.to_datetime(df['TimeInterval'])

# 計算一天中的第 n 個五分鐘
df['TimeIndex'] = df['TimeInterval'].dt.hour * 12 + df['TimeInterval'].dt.minute // 5 + 1

# 計算星期幾，0 代表星期日
df['WeekDay'] = df['TimeInterval'].dt.dayofweek

# 定義假日列表（假設格式為 'YYYY-MM-DD'）
holidays = ['2024-01-01', '2024-02-10', '2024-02-11', '2024-04-04', '2024-06-14', 
            '2024-10-10', '2024-10-11', '2024-12-25', '2024-01-31', '2024-09-29', 
            '2024-10-11']

holidays = pd.to_datetime(holidays)
df['Date'] = df['TimeInterval'].dt.date

# 計算是否是假日
df['HellDay'] = df['Date'].apply(lambda x: 1 if x in holidays or x.weekday() in [5, 6] else 0)

# 計算是否是假日前一天
df['HellDay'] = df.apply(lambda row: -1 if row['Date'] + pd.Timedelta(days=1) in holidays else row['HellDay'], axis=1)

# 提取 WayID 和 WayMilage
df['WayIDFrom'] = df['GantryFrom'].str[:3]
df['WayIDTo'] = df['GantryTo'].str[:3]
df['WayMilageFrom'] = pd.to_numeric(df['GantryFrom'].str[3:7], errors='coerce')
df = df.dropna(subset=['WayMilageFrom'])
df['WayMilageTo'] = pd.to_numeric(df['GantryTo'].str[3:7], errors='coerce')
df = df.dropna(subset=['WayMilageTo'])
df['WayDirectionFrom'] = df['GantryFrom'].str[7]
df['WayDirectionTo'] = df['GantryTo'].str[7]

# 定義速度分級函數
def speed_class(speed):
    if speed == 0:
        return 0
    elif speed < 20:
        return 1
    elif 20 <= speed < 40:
        return 2
    elif 40 <= speed < 60:
        return 3
    elif 60 <= speed < 80:
        return 4
    else:
        return 5

# 計算速度分級
df['SpeedClass'] = df[['小客車速度', '小貨車速度', '大客車速度', '大貨車速度', '聯結車速度']].max(axis=1).apply(speed_class)

# 將df print
print(df)

# 將df存成新的CSV檔
df.to_csv('20240521/download/M05A_20240101_feature.csv', index=False)