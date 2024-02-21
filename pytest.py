import pytest
import json
from app import app, db, Task
from tests.conftest import client




@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_should_status_code_ok(client):
	response = client.get('/get')
	assert response.status_code == 200
