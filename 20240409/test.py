#用pandas讀取CSV檔案，並提取經緯度資料
#CSV檔案的路徑是C:\\Users\\User\\Desktop\\cycu_ai2024\\20240409\\地震活動彙整_638482840836426113.csv
import pandas as pd
csv_path = 'C:\\Users\\User\\Desktop\\cycu_ai2024\\20240409\\地震活動彙整_638482840836426113.csv'
df = pd.read_csv(csv_path, encoding='big5')
print(df)
locations = df[['緯度', '經度']].values.tolist()
print(locations)
#提取經緯度資料後，將其轉換成list格式
#最後，將list格式的經緯度資料傳遞給index.html進行顯示


