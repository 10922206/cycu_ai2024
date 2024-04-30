import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def download_csv_files(url, download_path):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.csv'):
            file_url = urllib.parse.urljoin(url, href)
            file_name = os.path.join(download_path, os.path.basename(href))
            urllib.request.urlretrieve(file_url, file_name)

# 使用方式
base_url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240429/'
download_path = 'C:\\Users\\User\\Downloads\\M05A'

for i in range(0, 25):
    url = base_url + str(i).zfill(2) + '/'
    download_csv_files(url, download_path)