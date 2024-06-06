"""Приложение Fast API для модели прогнозирования стоимости квартиры"""


from fastapi import FastAPI, Body
from .fast_api_handler import FastApiHandler


# Создаю приложение Fast API
app = FastAPI()

# Создаю обработчик запросов для API
app.handler = FastApiHandler()


@app.post("/api/churn/") 
def get_prediction_for_item(
    build_id: int,
    model_params: dict = Body(
        example={
            'build_year': 1994,
            'building_type_int': '4',
            'latitude': 55.834713,
            'longitude': 37.448383,
            'ceiling_height': 2.64,
            'flats_count': 204,
            'floors_total': 17,
            'has_elevator': 1,
            'floor': 16,
            'kitchen_area': 10.10,
            'living_area': 44.799999,
            'rooms': 3,
            'total_area': 73.800003
        }
    )
):

  
    all_params = {
        "build_id": build_id,
        "model_params": model_params
    }
    return app.handler.handle(all_params)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8081)