import os
import tempfile
import json
import pytest
from app import create_app
from app.models import db, User, Task

@pytest.fixture
def client():
    app = create_app()
    app.config.from_object('config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # create a default user
            user = User(username='testuser', password='pbkdf2:sha256:150000$abc$abc')
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


def test_register_and_login(client):
    resp = client.post('/auth/register', json={'username': 'u1', 'password': 'pass'})
    assert resp.status_code == 201
    resp = client.post('/auth/login', json={'username': 'u1', 'password': 'pass'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'access_token' in data


def test_crud_tasks(client):
    # register and login
    client.post('/auth/register', json={'username': 'u2', 'password': 'pass'})
    resp = client.post('/auth/login', json={'username': 'u2', 'password': 'pass'})
    token = json.loads(resp.data)['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # create
    r = client.post('/tasks', json={'title': 'T1', 'description': 'D1'}, headers=headers)
    assert r.status_code == 201
    task = json.loads(r.data)
    task_id = task['id']

    # get
    r = client.get(f'/tasks/{task_id}')
    assert r.status_code == 200

    # update
    r = client.put(f'/tasks/{task_id}', json={'title': 'T1 Updated'}, headers=headers)
    assert r.status_code == 200

    # delete
    r = client.delete(f'/tasks/{task_id}', headers=headers)
    assert r.status_code == 204
