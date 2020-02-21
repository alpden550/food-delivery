import pytest
from flask import session
from flask_login import current_user

from food_delivery import create_app
from food_delivery.extensions import db
from food_delivery.models import Meal, User

app = create_app(config_name='testing')
db.create_all(app=app)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestMainRoutes:

    @classmethod
    def setup_class(cls):
        with app.app_context():
            meal = Meal(title='Meal')
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
        client.post('/auth/login/', data={'email': 'email', 'password': 'password'}, follow_redirects=True)
        response = client.get('/account')
        assert response.status_code == 200