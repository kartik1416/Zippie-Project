from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .routes import tasks_bp
from .auth import auth_bp
from .models import db
from .schemas import ma
from config import Config

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Task Manager API",
        "description": "API documentation for the Task Manager.",
        "version": "1.0.0"
    },
    "basePath": "/"
}

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    swagger = Swagger(app, template=swagger_template)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def home():
        # Render the single-page dashboard that uses the API for auth and tasks
        return render_template('index.html')

    return app
