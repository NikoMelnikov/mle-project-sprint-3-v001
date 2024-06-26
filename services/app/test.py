import unittest
from .handler import FastApiHandler
import pandas as pd
import random

#импортирую класс для тестирования
class TestFastApiHandler(unittest.TestCase):
    
    #создаю тестовые данные
    def setUp(self):
        self.handler = FastApiHandler()
        self.test_model_params = [
            {
                'build_year': random.randint(1900, 2024),
                'building_type_int': random.randint(0, 5),
                'latitude': random.uniform(55, 56),
                'longitude': random.uniform(37, 38),
                'ceiling_height': random.uniform(2.5, 9),
                'flats_count': random.randint(1, 5000),
                'floors_total': random.randint(1, 50),
                'has_elevator': random.choice([0, 1]),
                'floor': random.randint(1, 50),
                'kitchen_area': random.uniform(3, 150),
                'living_area': random.uniform(1, 400),
                'rooms': random.randint(1, 100),
                'total_area': random.uniform(1, 6000)
            }
        ]
        
    #определяю тестовый метод для проверки метода check_required_query_params класса FastApiHandler
    def test_check_required_query_params(self):
        query_params = {"request_id": 123, "model_params": self.test_model_params}
        self.assertTrue(self.handler.check_required_query_params(query_params))
        
    # проверяю метод check_required_query_params
    def test_check_required_model_params(self):
        self.assertTrue(self.handler.check_required_model_params(self.test_model_params))
        
    # проверяю валидацию параметров
    def test_validate_params(self):
        params = {
            "request_id": 123,
            "model_params": self.test_model_params
        }
        self.assertTrue(self.handler.validate_params(params))
        
    #проверяю обработчик
    def test_handle(self):
        params = {
            "request_id": 123,
            "model_params": self.test_model_params
        }
        response = self.handler.handle(params)
        self.assertIn("request_id", response)
        self.assertIn("cost", response)
        print(f"Response: {response}")
        
if __name__ == '__main__':
    unittest.main()
