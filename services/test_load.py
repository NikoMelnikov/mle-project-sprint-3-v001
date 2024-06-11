import pandas as pd
import subprocess
import random

# Создаем DataFrame со случайными данными для примера
data = {
    'build_year': [1994, 1960, 1977, 1970, 2014],
    'building_type_int': [4, 1, 0, 6, 4],
    'latitude': [55.834713, 55.701302, 55.851589, 55.876389, 55.734455],
    'longitude': [37.448383, 37.738918, 37.416008, 37.716415, 37.412422],
    'ceiling_height': [2.64, 2.80, 2.48, 2.64, 2.64],
    'flats_count': [204, 20, 168, 98, 274],
    'floors_total': [17, 5, 12, 9, 10],
    'has_elevator': [1, 0, 1, 1, 1],
    'floor': [16, 1, 9, 5, 9],
    'kitchen_area': [10.10, 6.00, 10.30, 6.50, 10.08],
    'living_area': [44.799999, 16.5, 44.0, 28.0, 45.72],
    'rooms': [3, 1, 3, 2, 3],
    'total_area': [73.800003, 32.0, 66.0, 40.0, 75.099998],
    'target': [13390000.0, 5500000.0, 9500000.0, 9950000.0, 18500000.0]
}

df = pd.DataFrame(data)

# Функция для генерации случайной строки из DataFrame и отправки ее по curl
def send_random_row():
    random_row = df.sample(n=1)
    random_row_json = random_row.to_dict(orient='records')
  
    curl_command = f'curl -X "POST" "http://127.0.0.1:8081/api/churn/?request_id=1" -H "accept: application/json" -H "Content-Type: application/json" -d '{random_row_json}''
  
    subprocess.run(curl_command, shell=True)

# Отправляем 10 случайных запросов
for _ in range(10):
    send_random_row()