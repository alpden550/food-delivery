from flask import Blueprint, flash, redirect, render_template, session

from food_delivery.models import Category, Meal

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    all_meals = Category.query.join(Category.meals)
    sushi = all_meals.filter(Category.title == 'sushi').first()
    pasta = all_meals.filter(Category.title == 'pasta').first()
    streetfood = all_meals.filter(Category.title == 'streetfood').first()
    pizza = all_meals.filter(Category.title == 'pizza').first()
    new = all_meals.filter(Category.title == 'new').first()
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
    meal = Meal.query.get_or_404(meal_id)
    cart = session.get('cart') or []
    cart.append(meal_id)
    session['cart'] = cart
    flash(f'Добавили {meal.title} в корзину!')
    return redirect('/')
