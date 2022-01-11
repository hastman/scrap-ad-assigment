from fastapi.testclient import TestClient
import pytest
import json
from main import app
from datetime import datetime
import os
client = TestClient(app)


@pytest.fixture
def prepare_basic_test():
    file_name = './test/fixture/{}.json'.format(
        datetime.now().strftime("%d%m%y%H%M"))
    with open(file_name, 'a+') as f:
        json.dump({"geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        67.91748046874999,
                        6.293458760393985
                    ],
                    [
                        66.2255859375,
                        2.3504147112508176
                    ],
                    [
                        69.63134765625,
                        2.3065056838291094
                    ],
                    [
                        69.71923828125,
                        4.762572524280281
                    ],
                    [
                        67.91748046874999,
                        6.293458760393985
                    ]
                ]
            ]
        }}, f)
    yield file_name
    os.remove(file_name)


def test_when_api_is_not_health_should_return_service_unavaliable_status_code():
    response = client.get("/health")
    assert response.status_code == 503


def test_when_api_is_health_should_return_ok_status_code(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    response = client.get("/health")
    assert response.status_code == 200


def test_when_call_secured_endoint_without_api_key_header_should_return_forbidden_status_code():
    response = client.post("/geofence/in_fence/0.0/0.0")
    assert response.status_code == 403


def test_when_call_secured_endoint_with_invalid_api_key_header_should_return_unauthorized_status_code(monkeypatch):
    monkeypatch.setenv('API_KEY', "1231232")
    response = client.post(
        "/geofence/in_fence/0.0/0.0", headers={"X-API-KEY": "222222"})
    assert response.status_code == 401


def test_when_send_point_and_not_exists_in_fence_should_return_not_found_status_code(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    monkeypatch.setenv('API_KEY', "222222")
    response = client.post(
        "/geofence/in_fence/0.0/0.0", headers={"X-API-KEY": "222222"})
    assert response.status_code == 404


def test_when_send_point_and_exists_in_fence_should_return_ok_no_content_status_code(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    monkeypatch.setenv('API_KEY', "222222")
    response = client.post(
        "/geofence/in_fence/68.247070/4.12728", headers={"X-API-KEY": "222222"})
    assert response.status_code == 200
    assert response.json()["threshold"] > -1
