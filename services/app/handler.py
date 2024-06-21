import os
import pickle
import logging
import sys
import pandas as pd
from dotenv import load_dotenv
dotenv_path = '../services/.env'
load_dotenv(dotenv_path)
from . import constants

# Настраиваю логгирование
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
)
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class FastApiHandler:
    #инициирую переменные класса
    def __init__(self):
        self.param_types = {
            "request_id": int,
            "model_params": list
        }

        self.model_path = os.path.abspath(os.getenv('MODEL_PATH'))
        self.load_model(model_path=self.model_path)
        
        self.required_model_params = constants.required_model_params
        
    #загружаю модель 
    def load_model(self, model_path: str):
        try:
            with open(os.path.abspath(model_path), "rb") as file:
                self.model = pickle.load(file)
            logger.debug('Model loaded sussesfully')
            return self.model
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            
    #получаю предсказания модели
    def churn_predict(self, model_params):
        return self.model.predict(model_params).tolist()
    #проверяю параметры запроса
    
    def check_required_query_params(self, query_params: dict) -> bool:
        if "request_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["request_id"], self.param_types["request_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True
    
    #проверяю наличие обязательных параметров модели
    def check_required_model_params(self, model_params: dict) -> bool:
        if set(model_params[0].keys()) == set(self.required_model_params):
            return True
        return False
    #валидирую запрос
    
    def validate_params(self, params: dict) -> bool:
        if self.check_required_query_params(params):
            logger.debug("All query params exist")
        else:
            logger.warning("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            logger.debug("All model params exist")
        else:
            logger.warning("Not all model params exist")
            return False
        return True
    
    #основная функция обработчик
    def handle(self, params):
        try:
            if not self.validate_params(params):
                logger.error("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = pd.DataFrame(params["model_params"]) #обращаю JSON бусурманский в датафрейм истинный
                request_id = params["request_id"]
                logger.info(f"Predicting for request_id: and model_params:\n{model_params}")
                cost = self.churn_predict(model_params)
                response = {
                    "request_id": request_id, 
                    "cost": cost
                }
        except Exception as e:
            logger.error(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response
#данные для тестирования работы класса
if __name__ == "__main__":
    test_params = {
    "request_id": 22,
    "model_params":[{
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
  }                    ]}
    
    handler = FastApiHandler()
    response = handler.handle(test_params)
    logger.info(f"Response: {response}")