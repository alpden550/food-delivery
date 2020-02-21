import random

import pytest
from faker import Faker

from food_delivery.extensions import db
from food_delivery.models import Category, Meal, User, Order
from tests.conftest import app

faker = Faker()


class TestModels:

    @classmethod
    def setup_class(cls):
        user = User(
            username=faker.profile()['username'],
            email=faker.email(),
            password=faker.password(),
        )
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        for _ in range(5):
            category = Category(title=faker.word(ext_word_list=None))
            with app.app_context():
                db.session.add(category)
                db.session.commit()

        with app.app_context():
            all_categories = Category.query.all()
        for _ in range(25):
            meal = Meal(
                title=faker.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                description=faker.text(max_nb_chars=200, ext_word_list=None),
                price=random.randint(100, 300),
                category=random.choice(all_categories),
            )
            with app.app_context():
                db.session.add(meal)
                db.session.commit()

        with app.app_context():
            all_meals = Meal.query.all()
        for _ in range(5):
            order = Order(
                amount=random.randint(300, 1000),
                client_name=faker.name(),
                client_address=faker.address(),
                client_email='email@gmail.com',
                meals=random.sample(all_meals, random.randint(3, 8)),
            )
            with app.app_context():
                db.session.add(order)
                db.session.commit()

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.session.query(User).delete()
            db.session.query(Category).delete()
            db.session.query(Meal).delete()
            db.session.query(Order).delete()
            db.session.commit()

    def test_meals_is_exist(self):
        with app.app_context():
            assert Meal.query.count() > 0

    def test_categories_exist(self):
        with app.app_context():
            assert Category.query.count() > 0

    def test_check_cart(self):
        with app.app_context():
            cart_items = random.sample([meal.id for meal in Meal.query.all()], 5)
            cart_meals = Meal.query.filter(Meal.id.in_(cart_items))
            cart_amount = sum(meal.price for meal in cart_meals)
        assert len(cart_items) == 5
        assert cart_meals.count() == 5
        assert cart_amount > 300

    def test_account_orders(self):
        with app.app_context():
            orders = Order.query.filter_by(client_email='email@gmail.com')
            for order in orders:
                assert 3 <= len(order.meals) <= 8
            assert orders.count() == 5

    def test_user(self):
        with app.app_context():
            assert User.query.first()
