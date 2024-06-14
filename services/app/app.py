"""Приложение Fast API для модели прогнозирования стоимости квартиры"""

import time
from fastapi import FastAPI, Body, HTTPException
from .handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

# Создаю приложение Fast API
app = FastAPI()

# Создаю обработчик запросов для API
app.handler = FastApiHandler()

# Инструментатор для prometheus
Instrumentator().instrument(app).expose(app)

# Создаю расчета времени предсказания
metric_prediction_time_counter = Counter(
    'app_time_exception_counter',
    'Total time spent processing requests'
)
# Метрика для распределения сумм предсказаний
metric_prediction_comparison = Histogram(
    'app_prediction_comparison',
    'Histogram for compare prediction value',
    buckets=[i * 600000 for i in range(51)] # в датасете минимальная стоимость составляла порядка 600000 
)
# Метрика для подсчета ошибочных запросов
metric_error_counter = Counter(
    'app_error_counter',
    'Total number of errors occurred',
)

@app.post("/api/predict/") 
def get_prediction_for_item(
    request_id: int,
    model_params: list = Body(
        [
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
                "kitchen_area": 10.10,
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
                "kitchen_area": 10.30,
                "living_area": 44.000000,
                "rooms": 3,
                "total_area": 66.000000
            }
        ]
    )
):
    try:
        start_time = time.time()
  
        all_params = {
                       "request_id": request_id,
                       "model_params": model_params
                     }
    
        response = app.handler.handle(all_params)
        end_time = time.time()
        processing_time = end_time - start_time
        metric_prediction_time_counter.inc(processing_time)
        for cost in response['cost']:
            metric_prediction_comparison.observe(cost)
        return response
    
    except Exception as e:
        metric_error_counter.inc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)