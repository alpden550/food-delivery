import click
from flask import Flask
from flask_admin.menu import MenuLink

from food_delivery.admin import UserView, CategoryView, MealView, OrderView
from food_delivery.blueprints.auth import auth_bp
from food_delivery.blueprints.main import main_bp
from food_delivery.db_utils import fill_db
from food_delivery.extensions import admin, csrf, db, login, migrate, toolbar
from food_delivery.models import User, Category, Meal, Order
from food_delivery.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_template_filters(app)
    register_admins()

    return app


def register_extensions(app):
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    login.init_app(app)
    admin.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_admins():
    admin.add_link(MenuLink(name='Вернуться на сайт', url='/'))
    admin.add_view(UserView(User, db.session, name='Пользователи'))
    admin.add_view(CategoryView(Category, db.session, name='Категории блюд'))
    admin.add_view(MealView(Meal, db.session, name='Блюда'))
    admin.add_view(OrderView(Order, db.session, name='Заказы'))


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

    @app.cli.command()
    @click.option('-n', '--name', default='admin', help='Username for admin')
    @click.option('-e', '--email', default='admin@gmail.com', help='Email for admin')
    @click.option('-p', '--password', default='1111', help='Password for admin')
    def superuser(name, email, password):
        """Create default admin."""
        admin = User(username=name, email=email, password=password, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        click.echo('Default admin was created.')


def register_template_filters(app):
    @app.template_filter('datetimeformat')
    def datetimeformat(date):
        return date.strftime('%d-%m-%Y')
