import pandas as pd
import os

# 指定資料夾路徑的基本部分
base_folder_path = '20240521\\download\\'

# 指定日期範圍
dates = pd.date_range(start='20240101', end='20240430').strftime('%Y%m%d')

# 使用迴圈遍歷每個日期
for date in dates:
    # 創建一個空的 DataFrame 來存儲所有的數據
    df = pd.DataFrame()

    # 指定當前日期的資料夾路徑
    folder_path = base_folder_path + date

    # 獲取資料夾中的所有檔案名稱
    file_names = os.listdir(folder_path)

    # 使用迴圈讀取和合併所有的 CSV 檔案
    for file_name in file_names:
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            temp_df = pd.read_csv(file_path, encoding='utf-8', header=None)
            df = pd.concat([df, temp_df])

    # 為 DataFrame 添加新的欄位名稱
    df.columns = ['TimeInterval', 'GantryFrom', 'GantryTo', 'VehicleType', 'SpaceMeanSpeed', '交通量']

    # 將合併後的 DataFrame 存成新的 CSV 檔
    df.to_csv(base_folder_path + date + '.csv', index=False)