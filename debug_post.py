from app import create_app
from app.models import db
import json

app = create_app()
app.config.from_object('config.TestingConfig')
with app.test_client() as c:
    with app.app_context():
        db.create_all()
    # register and login
    c.post('/auth/register', json={'username':'u2','password':'pass'})
    resp = c.post('/auth/login', json={'username':'u2','password':'pass'})
    print('login status', resp.status_code, resp.data)
    token = json.loads(resp.data)['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    r = c.post('/tasks', json={'title':'T1','description':'D1'}, headers=headers)
    print('create status', r.status_code)
    print(r.get_data(as_text=True))
    with app.app_context():
        db.drop_all()
