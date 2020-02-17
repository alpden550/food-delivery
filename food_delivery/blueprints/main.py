from random import sample

from flask import Blueprint, flash, redirect, render_template, session

from food_delivery.models import Category, Meal

main_bp = Blueprint('main', __name__)


@main_bp.route('/')  # noqa:R701
def index():
    categories = Category.query.join(Category.meals).all()
    sushi = [category for category in categories if category.title == 'sushi'][0]
    pasta = [category for category in categories if category.title == 'pasta'][0]
    streetfood = [category for category in categories if category.title == 'streetfood'][0]
    pizza = [category for category in categories if category.title == 'pizza'][0]
    new = [category for category in categories if category.title == 'new'][0]

    meals = Meal.query
    if session.get('cart') is not None:
        cart_items = set(session.get('cart'))
        cart_amount = sum((int(meals.get(meal).price) for meal in cart_items))
    return render_template(
        'main.html',
        sushi=sample(sushi.meals, 3),
        streetfood=sample(streetfood.meals, 3),
        pizza=sample(pizza.meals, 3),
        pasta=sample(pasta.meals, 3),
        new=sample(new.meals, 3),
        cart_items=cart_items,
        cart_amount=cart_amount,
    )


@main_bp.route('/addtocart/<int:meal_id>')
def add_to_cart(meal_id):
    session.permanent = True
    meal = Meal.query.get_or_404(meal_id)
    cart = session.get('cart') or []
    cart.append(meal_id)
    session['cart'] = cart
    flash(f'Добавили {meal.title} в корзину!')
    return redirect('/')
