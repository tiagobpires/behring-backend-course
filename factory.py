from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from spectree import SecurityScheme, SpecTree
from flask_jwt_extended import JWTManager
from sqlalchemy import select

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = SpecTree(
    "flask",
    title="Behring Backend Course API",
    version="v1.0",
    path="docs",
    security_schemes=[
        SecurityScheme(
            name="api_key",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )
    ],
    security={"api_key": []},
)


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from models import User

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @jwt.user_lookup_loader
    def user_load(header, data):
        current_user = db.session.scalars(
            select(User).filter_by(username=data["sub"])
        ).first()

        return current_user

    from controllers import user_controller, auth_controller

    app.register_blueprint(user_controller)
    app.register_blueprint(auth_controller)

    api.register(app)

    @app.route("/")
    def hello_world():
        return "<h1>Hello, World!</h1>"

    return app
