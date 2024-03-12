import csv
from collections import Counter

# 儲存第八列的數字
numbers = []

# 開啟CSV檔案，並使用'utf-8'編碼
with open('C:\\Users\\User\\Downloads\\112年1-10月交通事故簡訊通報資料.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳過標題行
    # 遍歷每一行
    for row in reader:
        # 檢查第八列的值是否為空
        if row[7]:
            # 將第八列的數字加入到列表中
            numbers.append(float(row[7]))

# 計算每個數字出現的次數
counter = Counter(numbers)

# 列印每個數字及其出現的次數
for number, count in counter.items():
    print(f'數字 {number} 出現了 {count} 次')
    #將結果寫入新的CSV檔案
    with open('C:\\Users\\User\\Downloads\\result.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['數字', '次數'])
        for number, count in counter.items():
            writer.writerow([number, count])
    
