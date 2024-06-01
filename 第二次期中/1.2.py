import pandas as pd

vehicle_types = {
    31: ('小客車', '小客車速度'),
    32: ('小貨車', '小貨車速度'),
    41: ('大客車', '大客車速度'),
    42: ('大貨車', '大貨車速度'),
    5:  ('聯結車', '聯結車速度')
}

# 指定檔案路徑的基本部分
base_file_path = '20240521/download/'

# 指定日期範圍
dates = pd.date_range(start='20240101', end='20240430').strftime('%Y%m%d')

# 使用迴圈遍歷每個日期
for date in dates:
    # 指定當前日期的檔案路徑
    file_path = base_file_path + date + '.csv'

    # 讀取CSV檔，使用UTF-8編碼
    df = pd.read_csv(file_path, encoding='utf-8')

    # 初始化新列
    for traffic_col, speed_col in vehicle_types.values():
        df[traffic_col] = 0
        df[speed_col] = 0

    # 使用布爾索引進行篩選並賦值
    for vtype, (traffic_col, speed_col) in vehicle_types.items():
        mask = df['VehicleType'] == vtype
        df.loc[mask, traffic_col] = df.loc[mask, '交通量']
        df.loc[mask, speed_col] = df.loc[mask, 'SpaceMeanSpeed']

    # 移除 'VehicleType' 和 'SpaceMeanSpeed' 列
    df = df.drop(columns=['VehicleType', 'SpaceMeanSpeed', '交通量'])

    # 將df print
    print(df)

    # 將df存成新的CSV檔
    df.to_csv(base_file_path + 'M05A_' + date + '.csv', index=False)
#以下是我的輸出結果
#            TimeInterval GantryFrom  GantryTo  VehicleType  SpaceMeanSpeed  交通量
#0       2024/01/01 00:00   01F0017N  01F0005N           31              90   15
#1       2024/01/01 00:00   01F0017N  01F0005N           32              93    3
#2       2024/01/01 00:00   01F0017N  01F0005N           41               0    0
#3       2024/01/01 00:00   01F0017N  01F0005N           42               0    0
#4       2024/01/01 00:00   01F0017N  01F0005N            5               0    0
#...                  ...        ...       ...          ...             ...  ...
#606235  2024/01/01 23:55   05F0438N  05FR143N           31             100    8
#606236  2024/01/01 23:55   05F0438N  05FR143N           32              99    4
#606237  2024/01/01 23:55   05F0438N  05FR143N           41               0    0
#606238  2024/01/01 23:55   05F0438N  05FR143N           42               0    0
#606239  2024/01/01 23:55   05F0438N  05FR143N            5               0    0

#合併檔案的格式需重新整理成以下的型態：
#- TimeInterval
#- GantryFrom
#- GantryTo
#- SpaceMeanSpeed（只要小客車 31)
#- 交通量(小客車 31) (欄位名稱 v31)
#- 交通量(小貨車 32) (欄位名稱 v32)
#- 交通量(大客車 41) (欄位名稱 v41)
#- 交通量(大貨車 42) (欄位名稱 v42)
#- 交通量(聯結車 5)  (欄位名稱 v5)

