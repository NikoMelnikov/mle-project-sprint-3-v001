import joblib
import pandas as pd
import json

class FastApiHandler:
    #инициирую переменные класса
    def __init__(self):
        self.param_types = {
            "build_id": int,
            "model_params": dict
        }

        self.model_path = "../services/model/model.pkl"
        self.load_churn_model(model_path=self.model_path)
        
        self.required_model_params = [
            'build_year', 'building_type_int', 'latitude', 'longitude',
            'ceiling_height', 'flats_count', 'floors_total', 'has_elevator',
            'floor', 'kitchen_area', 'living_area', 'rooms', 'total_area'
        ]
    #загружаю модель 
    def load_churn_model(self, model_path: str):
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")
    #получаю предсказания модели в виде числа
    def churn_predict(self, model_params):
        return int(self.model.predict(model_params).round(2)[0])
    #проверяю параметры запроса
    def check_required_query_params(self, query_params: dict) -> bool:
        if "build_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["build_id"], self.param_types["build_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True
    #проверяю наличие обязательных параметров модели
    def check_required_model_params(self, model_params: dict) -> bool:
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    #валидирую запрос
    def validate_params(self, params: dict) -> bool:
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
    #основная функция обработчик
    def handle(self, params):
        try:
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = pd.json_normalize(params["model_params"])
                build_id = params["build_id"]
                print(f"Predicting for build_id: and model_params:\n{model_params}")
                cost = self.churn_predict(model_params)
                response = {
                    "build_id": build_id, 
                    "cost": cost
                }
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response
#тестовые данные для проверки работы класса
if __name__ == "__main__":
    test_params = {
        "build_id": 22,
        "model_params": {
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
    }
    
    handler = FastApiHandler()
    response = handler.handle(test_params)
    print(f"Response: {response}")