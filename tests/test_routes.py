import pytest
from flask import session

from food_delivery.extensions import db
from food_delivery.models import Meal, User
from tests.conftest import app
from food_delivery.form import OrderForm


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestMainRoutes:

    @classmethod
    def setup_class(cls):
        with app.app_context():
            meal = Meal(title='Meal', price=100)
            db.session.add(meal)
            db.session.commit()

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            meal = Meal.query.first()
            db.session.delete(meal)
            db.session.commit()

    def test_index_page(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_cart_redirect(self, client):
        response = client.get('/cart')
        assert response.status_code == 308

    def test_cart_page(self, client):
        response = client.get('/cart/')
        assert response.status_code == 200

    def test_account_page(self, client):
        response = client.get('/account')
        assert response.status_code == 302

    def test_wrong_account(self, client):
        response = client.get('/account/')
        assert response.status_code == 404

    def test_add_to_cart_page(self, client):
        response = client.get('/addtocart/1')
        assert response.status_code == 302

    def teat_remove_from_cart_page(self, client):
        response = client.get('/delete/1')
        assert response.status_code == 302

    def test_ordered_page(self, client):
        response = client.get('/ordered')
        assert response.status_code == 200

    def test_add_to_cart_item(self, client):
        client.get('/addtocart/1')
        assert session.get('cart') == [1]

    def test_delete_item_from_cart(self, client):
        client.get('/addtocart/1')
        client.get('/delete/1')
        assert session.get('cart') == []

    def test_empty_cart(self, client):
        client.get('/')
        assert session.get('cart') is None

    def test_cart_sending(self, client):
        client.get('/addtocart/1')

        form = dict(name='Имя', address='Some address', email='email@gmail.com', phone='89261234567')
        response = client.post(
            '/cart/',
            data=form,
        )
        assert response.location == 'http://localhost/ordered'

    def test_cart_sending_not_valid(self, client):
        client.get('/addtocart/1')
        form = dict(name='Имя', address='Some address', email='email@gmail.com', phone='123')
        response = client.post(
            '/cart/',
            data=form,
        )
        assert response.location is None


class TestAuthRoutes:

    @classmethod
    def setup_class(cls):
        with app.app_context():
            admin = User(username='admin', is_admin=True, email='email', password='password')
            db.session.add(admin)
            db.session.commit()

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            admin = User.query.first()
            db.session.delete(admin)
            db.session.commit()

    def test_admin_redirect(self, client):
        response = client.get('/admin')
        assert response.status_code == 308

    def test_admin_page(self, client):
        response = client.get('/admin/')
        assert response.status_code == 302

    def test_login_page(self, client):
        response = client.get('/auth/login/')
        assert response.status_code == 200

    def test_registration_page(self, client):
        response = client.get('/auth/registration/')
        assert response.status_code == 200

    def test_logout(self, client):
        response = client.get('/auth/logout/')
        assert response.status_code == 302

    def test_user_can_admin(self, client):
        client.post(
            '/auth/login/',
            data={
                'email': 'email',
                'password': 'password'},
            follow_redirects=True)
        response = client.get('/admin')
        assert response.location == 'http://localhost/admin/'

    def test_user_can_login(self, client):
        client.post(
            '/auth/login/',
            data={
                'email': 'email',
                'password': 'password'},
            follow_redirects=True)
        response = client.get('/account')
        assert response.status_code == 200
