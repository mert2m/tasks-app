import pytest
import json
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_get_all_tasks_empty(client):
    response = client.get('/get')
    assert response.status_code == 200
    assert json.loads(response.data) == {'tasks': []}

def test_create_task(client):
    task_data = {'content': 'Task 1', 'completed': 'no'}
    response = client.post('/post', json=task_data)
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Task created successfully'}

    response = client.get('/get')
    assert response.status_code == 200
    assert json.loads(response.data) == {'tasks': [{'content': 'Task 1', 'completed': 'no'}]}

def test_delete_task(client):
    task_data = {'content': 'Task 1', 'completed': 'no'}
    client.post('/post', json=task_data)

    response = client.delete('/home/delete/Task 1')
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Task deleted successfully'}

    response = client.get('/get')
    assert response.status_code == 200
    assert json.loads(response.data) == {'tasks': []}
