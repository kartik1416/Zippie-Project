from app import create_app
from app.models import db

app = create_app()
app.config.from_object('config.DevelopmentConfig')
with app.app_context():
    db.create_all()
    print('DB tables created')
