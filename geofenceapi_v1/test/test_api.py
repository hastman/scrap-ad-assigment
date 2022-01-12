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


def test_when_not_exists_env_var_for_storage_location_should_returnt_service_unavailable():
    response = client.get("/health")
    assert response.status_code == 503


def test_when_exists_env_var_for_storage_location_but_is_not_a_folder_should_returnt_service_unavailable(monkeypatch):
    monkeypatch.setenv('STORAGE_LOCATION', '/tmp/')
    response = client.get("/health")
    assert response.status_code == 503


def test_when_api_is_health_should_return_ok_status_code(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    response = client.get("/health")
    assert response.status_code == 200


def test_when_call_secured_endoint_without_api_key_header_should_return_forbidden_status_code():
    response = client.post("/geofence/point", json={"x": 0.0, "y": 0.0})
    assert response.status_code == 403


def test_when_call_secured_endoint_with_invalid_api_key_header_should_return_unauthorized_status_code(monkeypatch):
    monkeypatch.setenv('API_KEY', "1231232")
    response = client.post(
        "/geofence/point", json={"x": 0.0, "y": 0.0}, headers={"X-API-KEY": "222222"})
    assert response.status_code == 401


def test_when_send_point_and_not_exists_in_fence_should_return_not_found_status_code(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    monkeypatch.setenv('API_KEY', "222222")
    response = client.post(
        "/geofence/point", json={"x": 0.0, "y": 0.0}, headers={"X-API-KEY": "222222"})
    assert response.status_code == 404


def test_when_send_point_and_exists_in_fence_should_return_ok_no_content_status_code(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    monkeypatch.setenv('API_KEY', "222222")
    response = client.post(
        "/geofence/point", json={"x": 68.247070, "y": 4.12728}, headers={"X-API-KEY": "222222"})
    assert response.status_code == 204


def test_when_try_to_update_fence_and_polygon_has_only_two_coordinates_should_return_bad_request(monkeypatch):
    monkeypatch.setenv('API_KEY', "222222")
    response = client.put(
        "/geofence", json={"points": [{"x": 0, "y": 0}, {"x": 1, "y": 0}]}, headers={"X-API-KEY": "222222"})
    assert response.status_code == 400
    assert response.json() == {"msg": "Invalid polygon, minimun three points"}


def test_when_try_to_update_fence_and_poligon_is_not_closed_should_return_bad_request(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('API_KEY', "222222")
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    response = client.put(
        "/geofence", json={"points": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 0, "y": 0}]}, headers={"X-API-KEY": "222222"})
    assert response.status_code == 400
    assert response.json() == {
        "msg": "Invalid polygon, coordenates must be closed"}


def test_when_try_to_update_fence_and_poligon_is_valid_should_return_status_code_no_content_and_polygon_must_be_updated(prepare_basic_test, monkeypatch):
    monkeypatch.setenv('API_KEY', "222222")
    monkeypatch.setenv('STORAGE_LOCATION', prepare_basic_test)
    response = client.put(
        "/geofence", json={"points": [{"x": 0, "y": 0}, {"x": 2, "y": 0}, {"x": 0, "y": 2}, {"x": 0, "y": 0}]}, headers={"X-API-KEY": "222222"})
    assert response.status_code == 204
    response = client.post(
        "/geofence/point", json={"x": 0.5, "y": 0.5}, headers={"X-API-KEY": "222222"})
    assert response.status_code == 204
