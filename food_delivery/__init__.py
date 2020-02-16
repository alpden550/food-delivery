from flask import Flask, render_template

from food_delivery.extensions import db, migrate
from food_delivery.models import User  # noqa:F401
from food_delivery.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    @app.route('/')
    def index():
        return render_template('account.html')

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
