import allure
import jsonschema
import requests
import pytest
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_place_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка данных на размещение заказа"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id']
            assert response_json['petId'] == payload['petId']
            assert response_json['quantity'] == payload['quantity']
            assert response_json['status'] == payload['status']
            assert response_json['complete'] == payload['complete']

    @allure.title("Получение информации о заказе по ID")
    def test_get_by_id(self, place_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = place_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_by_id(self, delete_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = delete_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200

        with allure.step("Удаление заказ по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_store(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step("Проверка данных инвентаря в ответе"):
            expected_data = {"approved": 57, "delivered": 50}

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_store(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и данных инвентаря магазина"):
            assert response.status_code == 200
            inventory_data = response.json()
            expected_data = {
                "approved": 57,
                "delivered": 50
            }
            assert inventory_data == expected_data