import click
from flask import Flask

from food_delivery.blueprints.main import main_bp
from food_delivery.db_utils import fill_db
from food_delivery.extensions import db, migrate, toolbar
from food_delivery.models import User  # noqa:F401
from food_delivery.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db, compare_type=True)


def register_blueprints(app):
    app.register_blueprint(main_bp)


def register_commands(app):
    @app.cli.command()
    def init():
        """Create empty database."""
        db.drop_all()
        db.create_all()
        click.echo('Initialized empty database.')

    @app.cli.command()
    def fill():
        """Add categories and meals."""
        fill_db()
