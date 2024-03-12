import csv
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

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

# 獲取數字和次數
numbers = list(counter.keys())
counts = list(counter.values())

# 找出次數最高的數字和次數
max_count = max(counts)
max_count_index = counts.index(max_count)
max_count_number = numbers[max_count_index]

# 設置字體為Microsoft JhengHei
font = FontProperties(fname=r"c:\windows\fonts\msjh.ttc", size=14)

# 繪製長條圖
plt.bar(numbers, counts)
plt.xlabel('數字', fontproperties=font)
plt.ylabel('次數', fontproperties=font)
plt.title('數字出現的次數', fontproperties=font)

# 設置x軸的範圍
plt.xlim([min(numbers), max(numbers)])

# 標示出次數最高的數字
plt.annotate(f'最高次數: {max_count}', 
             xy=(max_count_number, max_count), 
             xytext=(max_count_number, max_count + 5), 
             arrowprops=dict(facecolor='red', shrink=0.05),
             fontproperties=font)

# 顯示最高次數的x值和y值
print(f'最高次數的x值: {max_count_number}, y值: {max_count}')

plt.show()