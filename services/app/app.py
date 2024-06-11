"""Приложение Fast API для модели прогнозирования стоимости квартиры"""


from fastapi import FastAPI, Body
from .handler import FastApiHandler

# Создаю приложение Fast API
app = FastAPI()

# Создаю обработчик запросов для API
app.handler = FastApiHandler()


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

  
    all_params = {
        "request_id": request_id,
        "model_params": model_params
    }
    return app.handler.handle(all_params)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)