# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружение

python3 -m venv .mle-project-sprint-3-v001-venv
source .mle-project-sprint-3-v001-venv/bin/activate
pip install fastapi
 pip install "uvicorn[standard]"

#### Для проверки работы функции обработчика:

python -m app.fast_api_handler

Ожидаемый ответ:

All query params exist
All model params exist
Predicting for build_id: and model_params:
   build_year building_type_int   latitude  longitude  ...  kitchen_area  living_area  rooms  total_area
0        1994                 4  55.834713  37.448383  ...          10.1    44.799999      3   73.800003

[1 rows x 13 columns]
Response: {'build_id': 22, 'cost': 16073731}

#### Для запуска сервиса fast api:

python -m app.churn_app.py

Документация по методу:

http://127.0.0.1:8081/docs

Пример curl запроса:

curl -X 'POST' \
  'http://127.0.0.1:8081/api/churn/?build_id=22' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "build_year": 1994,
  "building_type_int": "4",
  "latitude": 55.834713,
  "longitude": 37.448383,
  "ceiling_height": 2.64,
  "flats_count": 204,
  "floors_total": 17,
  "has_elevator": 1,
  "floor": 16,
  "kitchen_area": 10.1,
  "living_area": 44.799999,
  "rooms": 3,
  "total_area": 73.800003
}'

Ожидаемый ответ:

{"build_id":22,"cost":16073731}

### 2. FastAPI микросервис в Docker-контейнере
...
