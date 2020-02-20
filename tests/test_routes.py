import pytest

from food_delivery import create_app

app = create_app()


@pytest.fixture
def flask_app():
    app.testing = True
    client = app.test_client()
    yield client


class TestMainRoutes:

    def test_index(self, flask_app):
        response = flask_app.get('/')
        assert response.status_code == 200

    def test_cart_redirect(self, flask_app):
        response = flask_app.get('/cart')
        assert response.status_code == 308

    def test_cart(self, flask_app):
        response = flask_app.get('/cart/')
        assert response.status_code == 200

    def test_account(self, flask_app):
        response = flask_app.get('/account')
        assert response.status_code == 302

    def test_wrong_account(self, flask_app):
        response = flask_app.get('/account/')
        assert response.status_code == 404

    def test_add_to_cart(self, flask_app):
        response = flask_app.get('/addtocart/1')
        assert response.status_code == 302

    def teat_remove_from_cart(self, flask_app):
        response = flask_app.get('/delete/1')
        assert response.status_code == 302

    def test_ordered(self, flask_app):
        response = flask_app.get('/ordered')
        assert response.status_code == 200


class TestAuthRoutes:
    def test_admin_redirect(self, flask_app):
        response = flask_app.get('/admin')
        assert response.status_code == 308

    def test_admin(self, flask_app):
        response = flask_app.get('/admin/')
        assert response.status_code == 302

    def test_login(self, flask_app):
        response = flask_app.get('/auth/login/')
        assert response.status_code == 200

    def test_registration(self, flask_app):
        response = flask_app.get('/auth/registration/')
        assert response.status_code == 200

    def test_logout(self, flask_app):
        response = flask_app.get('/auth/logout/')
        assert response.status_code == 302
