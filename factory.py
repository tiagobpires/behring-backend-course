from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from models import User

    db.init_app(app)
    migrate.init_app(app, db)

    from controllers import user_controller

    app.register_blueprint(user_controller)

    @app.route("/")
    def hello_world():
        return "<h1>Hello, World!</h1>"

    return app
