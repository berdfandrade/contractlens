from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "ContractLens API is alive"


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World from /api"

