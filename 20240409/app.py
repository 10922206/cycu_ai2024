from flask import Flask, render_template, jsonify
import pandas as pd
import webbrowser
import threading

app = Flask(__name__)

# 全域變數，用於追蹤是否已經打開過瀏覽器
first_request = True

def open_browser():
    webbrowser.open_new('http://localhost:5000/')

@app.route('/')
def index():
    global first_request
    if first_request:
        # 在新的瀏覽器視窗或標籤中打開 Flask 應用程式的 URL
        threading.Timer(1, open_browser).start()
        first_request = False

    # 讀取 CSV 檔案
    csv_path = 'C:\\Users\\User\\Desktop\\cycu_ai2024\\20240409\\地震活動彙整_638482840836426113.csv'
    df = pd.read_csv(csv_path, encoding='big5', usecols=['編號', '地震時間', '規模', '深度', '緯度', '經度'])
    
    locations = df[['緯度', '經度']].values.tolist()
    earthquake_info = df[['編號', '地震時間', '規模', '深度']].values.tolist()
    
    return render_template('index.html', locations=locations, earthquake_info=earthquake_info)

@app.route('/data')
def get_data():
    # 讀取 CSV 檔案
    csv_path = 'C:\\Users\\User\\Desktop\\cycu_ai2024\\20240409\\地震活動彙整_638482840836426113.csv'
    df = pd.read_csv(csv_path, encoding='big5', usecols=['編號', '地震時間', '規模', '深度', '緯度', '經度'])
    
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)