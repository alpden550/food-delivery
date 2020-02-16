from flask import Blueprint, render_template

from food_delivery.models import Category

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
