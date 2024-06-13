import pandas as pd
import requests
import json
import time
import random

# Чтение файла с примером данных в директории services/models
df = pd.read_csv('/home/mle-user/mle_projects/mle-project-sprint-3-v001/services/models/X_example.csv')
print(df)

url = "http://localhost:4601/api/predict/?request_id=1"
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}
#формирую последовательные запросы имитирующие работу сервиса
for index, row in df.iterrows():
    payload = json.dumps([row.to_dict()])
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    
    # Генерация случайного времени ожидания от 1 до 5 секунд
    timeout = random.uniform(1, 5)
    time.sleep(timeout)