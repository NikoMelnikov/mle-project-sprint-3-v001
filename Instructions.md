# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружение

Модель сохранена с помощью MLflow в формате pkl. Загрузка модели в приложение осуществляется 
с помощью модуля  pickle, загрузка с использованием joblift приводила к ошибкам.

В корневой директории создается виртуальное пространство и устанавливаются зависимости.

python3 -m venv .mle-project-sprint-3-v001-venv
source .mle-project-sprint-3-v001-venv/bin/activate
pip install -r requirements.txt

В директории app создано приложение app - приложение Fast API для модели прогнозирования стоимости квартиры которое в свою очередь использует приложение обработчик handler.

#### Для тестирования работоспособности функции обработчика:
Протестировать обработчик напрямую возможно запустив скрипт:
$ python -m app.handler

Также попробовал подготовить юниттестирование, запустить можно по скрипту:
$ python -m app.test

Ожидаемый ответ:

2024-06-11 08:45:45,650 : DEBUG : root : Model loaded sussesfully
2024-06-11 08:45:45,651 : DEBUG : root : All query params exist
2024-06-11 08:45:45,651 : DEBUG : root : All model params exist
2024-06-11 08:45:45,663 : INFO : root : Predicting for request_id: and model_params:
   build_year  building_type_int   latitude  longitude  ceiling_height  ...  floor  kitchen_area  living_area  rooms  total_area
0        1994                  4  55.834713  37.448383            2.64  ...     16          10.1    44.799999      3   73.800003
1        1977                  0  55.851589  37.416008            2.48  ...      9          10.3    44.000000      3   66.000000

[2 rows x 13 columns]
2024-06-11 08:45:45,666 : INFO : root : Response: {'request_id': 22, 'cost': [16070065.957960542, 12688998.272761442]}

#### Для запуска сервиса fast api:

$ python -m app.app

Документация по методу:

http://127.0.0.1:8081/docs

Предусмотрена отправка как одинарного запроса, так и множественного в массиве JSON. Каждый запрос помечается request_id для возможности дальнейшего логирования в третьих системах.
Пример curl запроса :

curl -X 'POST' \
  'http://localhost:4601/api/predict/?request_id=44' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "build_year": 1994,
    "building_type_int": 4,
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
  },
  {
    "build_year": 1977,
    "building_type_int": 0,
    "latitude": 55.851589,
    "longitude": 37.416008,
    "ceiling_height": 2.48,
    "flats_count": 168,
    "floors_total": 12,
    "has_elevator": 1,
    "floor": 9,
    "kitchen_area": 10.3,
    "living_area": 44,
    "rooms": 3,
    "total_area": 66
  }
]'

Ожидаемый ответ:

{
  "request_id": 44,
  "cost": [
    16070065.957960542,
    12688998.272761442
  ]
}

### 2. FastAPI микросервис в Docker-контейнере
Собираем образ:

$ docker image build -f /home/mle-user/mle_projects/mle-project-sprint-3-v001/services/Dockerfile_ml_service . --tag services:with_env

Запускаем:

$ docker container run --publish 4601:8081 --volume=./models:/services/models   --env-file .env services:with_env

Проверяем доступность метода:

http://localhost:4601/docs

Ожидаемый вывод в консоли при пинге и успешной загрузке модели:

INFO:     Will watch for changes in these directories: ['/services']
INFO:     Uvicorn running on http://0.0.0.0:8081 (Press CTRL+C to quit)
INFO:     Started reloader process [7] using statreload
2024-06-11 08:48:33,709 : DEBUG : root : Model loaded sussesfully
2024-06-11 08:48:33,712 : INFO : uvicorn.error : Started server process [9]
2024-06-11 08:48:33,712 : INFO : uvicorn.error : Waiting for application startup.
INFO:     Started server process [9]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
2024-06-11 08:48:33,712 : INFO : uvicorn.error : Application startup complete.
INFO:     172.17.0.1:40984 - "GET /docs HTTP/1.1" 200 OK
INFO:     172.17.0.1:40984 - "GET /openapi.json HTTP/1.1" 200 OK
2024-06-11 08:49:08,491 : DEBUG : root : All query params exist
2024-06-11 08:49:08,491 : DEBUG : root : All model params exist
Predicting for request_id: and model_params:
   build_year  building_type_int   latitude  ...  living_area  rooms  total_area
0        1994                  4  55.834713  ...    44.799999      3   73.800003
1        1977                  0  55.851589  ...    44.000000      3   66.000000

[2 rows x 13 columns]
INFO:     172.17.0.1:40998 - "POST /api/predict/?request_id=44 HTTP/1.1" 200 OK

Остановка контейнера:
$ docker container ps
$ docker container stop  <<CONTAINER ID>>

#### Для запуска с использованием docker-compose:
$ docker compose up  --build
$ docker compose stop
$ docker compose down

http://localhost:9090/targets

$ python -m app.test_load