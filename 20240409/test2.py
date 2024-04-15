import csv

def read_earthquake_data(csv_file):
    earthquake_data = []
    with open(csv_file, 'r', encoding='big5') as file:
        reader = csv.DictReader(file)
        for row in reader:
            earthquake_data.append(row)
    return list(reversed(earthquake_data))  # 反轉資料順序

def generate_html(earthquake_data):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>地震資料地圖</title>
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.css" />
        <style>
            #map { height: 600px; }
            .custom-marker {
                background-color: transparent;
                border: none;
                width: 10px;
                height: 10px;
            }
        </style>
    </head>
    <body>
        <h1>地震資料地圖</h1>
        <div id="map"></div>
        <input type="range" min="0" max=""" + str(len(earthquake_data)) + """ value="0" id="slider"> <!-- 拉桿控制地震時間 -->
        <button onclick="play()">播放</button>
        <button onclick="stop()">停止</button>
        <button onclick="showAll()">顯示所有地震</button>
        <select id="speed">
            <option value="1000">正常</option>
            <option value="250">加快</option>
            <option value="1500">減緩</option>
        </select>
        <script>
            var map = L.map('map').setView([23.6978, 120.9605], 7);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
            }).addTo(map);

            var earthquakeData = """ + str(earthquake_data) + """;
            var index = 0;
            var slider = document.getElementById('slider');
            var speed = document.getElementById('speed').value;
            var timer;

            function showEarthquake() {
                if (index < earthquakeData.length) {
                    var earthquake = earthquakeData[index];
                    var magnitude = parseFloat(earthquake['規模']);
                    var color = 'green';
                    if (magnitude >= 5) {
                        color = 'red';
                    } else if (magnitude >= 4.5) {
                        color = 'orange';
                    }
                    var marker = L.marker([earthquake['緯度'], earthquake['經度']], {icon: L.divIcon({className: 'custom-marker', html: '<div style="background-color: ' + color + '; width: 10px; height: 10px; border-radius: 50%; opacity: 0.7;"></div>'})}).addTo(map);
                    marker.bindPopup("<b>" + earthquake['位置'] + "</b><br />規模: " + earthquake['規模'] + "<br />深度: " + earthquake['深度'] + "<br />時間: " + earthquake['地震時間']).openPopup();
                    slider.value = index;
                    index++;
                } else {
                    clearInterval(timer);
                }
            }

            function updateEarthquake() {
                index = slider.value;
                showEarthquake();
            }

            function play() {
                if (!timer) {
                    timer = setInterval(showEarthquake, speed);
                }
            }

            function stop() {
                clearInterval(timer);
                timer = null;
            }

            function showAll() {
                stop();
                for (var i = 0; i < earthquakeData.length; i++) {
                    var earthquake = earthquakeData[i];
                    var magnitude = parseFloat(earthquake['規模']);
                    var color = 'green';
                    if (magnitude >= 5) {
                        color = 'red';
                    } else if (magnitude >= 4.5) {
                        color = 'orange';
                    }
                    var marker = L.marker([earthquake['緯度'], earthquake['經度']], {icon: L.divIcon({className: 'custom-marker', html: '<div style="background-color: ' + color + '; width: 10px; height: 10px; border-radius: 50%; opacity: 0.7;"></div>'})}).addTo(map);
                    marker.bindPopup("<b>" + earthquake['位置'] + "</b><br />規模: " + earthquake['規模'] + "<br />深度: " + earthquake['深度'] + "<br />時間: " + earthquake['地震時間']).openPopup();
                }
            }

            function changeSpeed() {
                speed = document.getElementById('speed').value;
                if (timer) {
                    clearInterval(timer);
                    timer = setInterval(showEarthquake, speed);
                }
            }

            slider.addEventListener('input', updateEarthquake);
            document.getElementById('speed').addEventListener('change', changeSpeed);

        </script>
    </body>
    </html>
    """

    return html_content

def main():
    csv_file = 'earthquake_data.csv'
    earthquake_data = read_earthquake_data(csv_file)
    html_content = generate_html(earthquake_data)

    with open('earthquake_map.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("HTML檔案已生成")

if __name__ == "__main__":
    main()





