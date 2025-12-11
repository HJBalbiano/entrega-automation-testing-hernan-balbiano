from pathlib import Path

import pytest
import requests

from utils.data_loader import load_json


BASE_URL = "https://reqres.in/api"
DATA_DIR = Path(__file__).parent / "data"
CREATE_PAYLOAD = load_json(DATA_DIR / "create_user.json")


@pytest.mark.api
def test_get_users_should_return_list():
    response = requests.get(f"{BASE_URL}/users", params={"page": 2})
    assert response.status_code == 200
    body = response.json()
    assert "data" in body and isinstance(body["data"], list)
    assert body["data"], "La lista de usuarios no debería estar vacía"
    assert all("email" in user for user in body["data"])


@pytest.mark.api
def test_create_user_should_return_id_and_timestamp():
    response = requests.post(f"{BASE_URL}/users", json=CREATE_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body.get("name") == CREATE_PAYLOAD["name"]
    assert body.get("job") == CREATE_PAYLOAD["job"]
    assert "id" in body and "createdAt" in body


@pytest.mark.api
def test_delete_user_returns_204():
    response = requests.delete(f"{BASE_URL}/users/2")
    assert response.status_code == 204
    assert response.text == ""


@pytest.mark.api
def test_create_then_delete_user_chain():
    create_resp = requests.post(f"{BASE_URL}/users", json=CREATE_PAYLOAD)
    assert create_resp.status_code == 201
    user_id = create_resp.json().get("id")
    assert user_id is not None

    delete_resp = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert delete_resp.status_code == 204
