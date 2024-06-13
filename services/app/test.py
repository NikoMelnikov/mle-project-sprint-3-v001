import unittest
from .handler import FastApiHandler
import pandas as pd

#импортирую класс для тестирования
class TestFastApiHandler(unittest.TestCase):
    #создаю тестовые данные
    def setUp(self):
        self.handler = FastApiHandler()
        self.test_model_params = [
            {
                'build_year': 2020, 'building_type_int': 1, 'latitude': 55.7522, 
                'longitude': 37.6156, 'ceiling_height': 3.0, 'flats_count': 100, 
                'floors_total': 10, 'has_elevator': 1, 'floor': 5, 
                'kitchen_area': 12.0, 'living_area': 30.0, 'rooms': 1, 'total_area': 50.0
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
