from flask import Flask
from dotenv import load_dotenv
import os

from app.models import db
from .routes import blueprints

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///course.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)

    from .scripts.seeder import seed_all

    app.cli.add_command(seed_all)

    return app
