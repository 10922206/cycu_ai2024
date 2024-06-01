import requests
import os
from datetime import datetime, timedelta

def download_file(download_url, file_path):
    try:
        # 发送HTTP请求下载文件
        response = requests.get(download_url)
        response.raise_for_status()  # 检查请求是否成功

        # 将文件内容写入本地文件
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"文件已下载并保存至: {file_path}")
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f"文件未找到: {download_url}")
        return False
    except Exception as err:
        print(f"其他错误: {err}")
        return False

import tarfile

def download_files_for_date(date, save_dir='20240521/download/'):
    # 创建日期子目录
    save_dir = os.path.join(save_dir, date)
    os.makedirs(save_dir, exist_ok=True)

    # 下载 .tar.gz 文件
    base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/"
    file_name = f"M05A_{date}.tar.gz"
    download_url = base_url + file_name
    file_path = os.path.join(save_dir, file_name)
    
    # 尝试下载 .tar.gz 文件
    if download_file(download_url, file_path):
        # 如果 .tar.gz 文件下载成功，解压文件
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(path=save_dir)
        print(f"文件已解压至: {save_dir}")

        # 解压完成后删除 .tar.gz 文件
        os.remove(file_path)
        print(f"已删除文件: {file_path}")
    else:
        # 如果 .tar.gz 文件下载失败，尝试下载 .csv 文件
        download_csv_files(date, save_dir)

def download_csv_files(date, save_dir='20240521/download/'):
    # 创建日期子目录
    save_dir = os.path.join(save_dir, date)
    os.makedirs(save_dir, exist_ok=True)

    base_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{date}/"
    
    for hour in range(24):
        hour_str = f"{hour:02d}"  # 小时格式化为两位数，例如 01、02 等
        for minute in range(0, 60, 5):  # 从0到55以5为间隔遍历分钟数
            minute_str = f"{minute:02d}00"
            file_name = f"TDCS_M05A_{date}_{hour_str}{minute_str}.csv"
            download_url = base_url + hour_str + '/' + file_name
            file_path = os.path.join(save_dir, file_name)
            download_file(download_url, file_path)

def download_files_in_range(start_date, end_date, save_dir='20240521/download'):
    # 将字符串日期转换为 datetime 对象
    start_dt = datetime.strptime(start_date, "%Y%m%d")
    end_dt = datetime.strptime(end_date, "%Y%m%d")
    
    # 遍历日期范围
    current_dt = start_dt
    while current_dt <= end_dt:
        date_str = current_dt.strftime("%Y%m%d")
        download_files_for_date(date_str, save_dir)
        current_dt += timedelta(days=1)

# 示例：下载2024年4月18日到2024年4月20日的文件
download_files_in_range("20240101", "20240430")

import os
import shutil
import datetime

start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 4, 30)
delta = datetime.timedelta(days=1)

base_dir = "C:\\Users\\andre\\Desktop\\cycu_ai2024\\第二次期中\\20240521\\download\\"

while start_date <= end_date:
    root_dir = os.path.join(base_dir, start_date.strftime("%Y%m%d"))

    # 遍歷並移動所有的CSV檔案
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.csv'):
                target_path = os.path.join(root_dir, filename)
                if not os.path.exists(target_path):  # 檢查目標位置是否已經存在一個同名的檔案
                    shutil.move(os.path.join(foldername, filename), root_dir)

    # 遍歷並刪除所有的空資料夾
    for foldername, subfolders, filenames in os.walk(root_dir, topdown=False):
        if not os.listdir(foldername):
            os.rmdir(foldername)

    start_date += delta