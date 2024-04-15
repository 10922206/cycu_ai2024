import csv

def read_earthquake_data(csv_file):
    earthquake_data = []
    with open(csv_file, 'r', encoding='big5') as file:
        reader = csv.DictReader(file)
        for row in reader:
            earthquake_data.append(row)
    return earthquake_data

def generate_html(earthquake_data):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>地震資料地圖</title>
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.css" />
        <style>
            #map { height: 400px; }
        </style>
    </head>
    <body>
        <h1>地震資料地圖</h1>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([0, 0], 2);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
            }).addTo(map);
    """

    for earthquake in earthquake_data:
        html_content += f"""
            L.marker([{earthquake['緯度']}, {earthquake['經度']}]).addTo(map)
                .bindPopup("<b>{earthquake['位置']}</b><br />規模: {earthquake['規模']}<br />深度: {earthquake['深度']}<br />時間: {earthquake['地震時間']}");
        """

    html_content += """
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
