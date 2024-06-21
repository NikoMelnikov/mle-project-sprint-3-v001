"""Приложение Fast API для модели прогнозирования стоимости квартиры"""

import time
from fastapi import FastAPI, Body, HTTPException
from .handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
from . import constants

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
    model_params: list = Body(constants.default_params)
    
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