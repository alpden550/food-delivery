from random import sample

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required

from food_delivery.extensions import db
from food_delivery.form import OrderForm
from food_delivery.models import Category, Meal, Order
from food_delivery.utils import check_cart

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    categories = {}
    for category in Category.query:
        meals = (
            sample(category.meals, 3) if len(category.meals) >= 3 else category.meals
        )
        categories[category.title] = meals

    cart = check_cart()

    return render_template('main.html', categories=categories, cart=cart)


@main_bp.route('/cart/', methods=('GET', 'POST'))
def cart():
    cart = check_cart()

    form = OrderForm()
    if request.method == 'POST' and form.validate_on_submit():
        order = Order(
            client_name=form.name.data,
            client_address=form.address.data,
            client_email=form.email.data,
            client_phone=form.phone.data,
            amount=cart.amount,
        )
        order.meals.extend(cart.meals)
        db.session.add(order)
        db.session.commit()
        session.pop('cart')
        return redirect(url_for('main.ordered'))
    return render_template('cart.html', cart=cart, form=form, meals=cart.meals)


@main_bp.route('/addtocart/<int:meal_id>')
def add_to_cart(meal_id):
    session.permanent = True
    meal = Meal.query.get_or_404(meal_id)
    cart = session.get('cart') or []
    cart.append(meal_id)
    session['cart'] = cart
    flash(f'Добавили {meal.title} в корзину!', 'success')
    return redirect('/')


@main_bp.route('/delete/<int:meal_id>')
def delete_from_cart(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    session.get('cart').remove(meal_id)
    flash(f'Удалили {meal.title} из корзины!', 'warning')
    return redirect(url_for('main.cart'))


@main_bp.route('/account')
@login_required
def account():
    cart = check_cart()
    orders = Order.query.filter_by(client_email=current_user.email).order_by(
        Order.created_at.desc(),
    )
    return render_template('account.html', orders=orders, cart=cart)


@main_bp.route('/ordered')
def ordered():
    return render_template('ordered.html')
