import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from scipy.interpolate import griddata

# 讀取CSV文件
df = pd.read_csv('20240521\download\M05A_20240429_feature.csv')
# 篩選資料
df = df[df['WayDirectionFrom'] == 'S']
df = df[df['WayIDFrom'] == '01F']
# 篩選必要的欄位
df = df[['TimeIndex', 'WayMilageFrom', '小客車','小客車速度']]


df_group1 = df.groupby(['WayMilageFrom', 'TimeIndex'])['小客車'].sum().reset_index()
df_group2 = df.groupby(['WayMilageFrom', 'TimeIndex'])['小客車速度'].sum().reset_index()
df = pd.merge(df_group1, df_group2, on=['WayMilageFrom', 'TimeIndex'])
# 將WayMilageFrom轉換為int
df['WayMilageFrom'] = df['WayMilageFrom'].astype(int)



# 準備Plotly的數據
data = np.array([df['TimeIndex'], df['WayMilageFrom'], df['小客車'],df['小客車速度']]).T
print(data)

#將data存成csv檔
df.to_csv('20240521\download\M05A_test.csv', index=False)

# 為插值進行網格化數據
x = np.linspace(data[:, 0].min(), data[:, 0].max(), num=50)
y = np.linspace(data[:, 1].min(), data[:, 1].max(), num=50)
x, y = np.meshgrid(x, y)
print(x)
# 使用 CubicSpline 進行插值
def interpolate_griddata(x, y, z, x_new, y_new):
    return griddata((x, y), z, (x_new, y_new), method='cubic')

# 準備插值數據
z_volume = interpolate_griddata(data[:, 0], data[:, 1], data[:, 2], x, y)
z_speed = interpolate_griddata(data[:, 0], data[:, 1], data[:, 3], x, y)

# 確保插值後的車速在合理範圍內
z_speed = np.clip(z_speed, 0, 120)

# 創建交通量圖形
fig_volume = go.Figure()

# 添加交通量表面
fig_volume.add_trace(go.Surface(z=z_volume, x=x, y=y, colorscale='Viridis', name='交通量'))

# 更新佈局以更好地視覺化
fig_volume.update_layout(
    title="2024年4月29日的交通量",
    scene=dict(
        xaxis_title='時間（小時）',
        yaxis_title='里程',
        zaxis_title='交通量',
        zaxis=dict(range=[0, z_volume.max()])  # 確保Z軸不顯示負值
    )
)

# 創建車速圖形
fig_speed = go.Figure()

# 添加車速表面
fig_speed.add_trace(go.Surface(z=z_speed, x=x, y=y, colorscale='RdYlBu', name='車速'))

# 更新佈局以更好地視覺化
fig_speed.update_layout(
    title="2024年4月29日的車速",
    scene=dict(
        xaxis_title='第幾個5分鐘',
        yaxis_title='里程',
        zaxis_title='車速',
        zaxis=dict(range=[0, 120])  # 確保Z軸不顯示超過120的值
    )
)

# 將圖保存為HTML文件
pio.write_html(fig_volume, file='traffic_volume.html', auto_open=False, include_plotlyjs='cdn')
pio.write_html(fig_speed, file='traffic_speed.html', auto_open=False, include_plotlyjs='cdn')

# 合併兩個HTML文件
with open('traffic_volume_speed.html', 'w', encoding='utf-8') as f:
    f.write('<html><head><title>2024年4月29日的交通量和車速</title></head><body>\n')
    f.write('<h1>2024年4月29日的交通量和車速 頁面最下方的圖片為車速關係圖</h1>\n')
    with open('traffic_volume.html', 'r', encoding='utf-8') as f_volume:
        f.write(f_volume.read())
    f.write('<h1>2024年4月29日的交通量和車速</h1>\n')
    with open('traffic_speed.html', 'r', encoding='utf-8') as f_speed:
        f.write(f_speed.read())
    f.write('</body></html>')

# 自動打開合併的HTML文件
import webbrowser
webbrowser.open('traffic_volume_speed.html')

