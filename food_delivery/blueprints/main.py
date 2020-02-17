from flask import Blueprint, flash, redirect, render_template, session

from food_delivery.models import Category, Meal

main_bp = Blueprint('main', __name__)


@main_bp.route('/')  # noqa:R701
def index():
    all_meals = Category.query.join(Category.meals).all()
    sushi = [category for category in all_meals if category.title == 'sushi'][0]
    pasta = [category for category in all_meals if category.title == 'pasta'][0]
    streetfood = [category for category in all_meals if category.title == 'streetfood'][0]
    pizza = [category for category in all_meals if category.title == 'pizza'][0]
    new = [category for category in all_meals if category.title == 'new'][0]
    return render_template(
        'main.html',
        sushi=sushi.meals,
        streetfood=streetfood.meals,
        pizza=pizza.meals,
        pasta=pasta.meals,
        new=new.meals,
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
