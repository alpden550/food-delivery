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

from food_delivery.form import OrderForm
from food_delivery.models import Category, Meal, Order
from food_delivery.extensions import db
from flask_login import current_user, login_required

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
        cart_amount = sum(meals.get(meal).price for meal in cart_items)
    else:
        cart_items, cart_amount = [], 0
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


@main_bp.route('/cart/', methods=('GET', 'POST'))
def cart():
    if session.get('cart') is not None:
        cart_items = set(session.get('cart'))
        meals = Meal.query.filter(Meal.id.in_(cart_items)).all()
        cart_amount = sum(meal.price for meal in meals)

    else:
        cart_items, cart_amount, meals = [], 0, []

    form = OrderForm()
    if request.method == 'POST' and form.validate_on_submit():
        order = Order(
            client_name=form.name.data,
            client_address=form.address.data,
            client_email=form.email.data,
            client_phone=form.phone.data,
            amount=cart_amount,
        )
        order.meals.extend(meals)
        db.session.add(order)
        db.session.commit()
        session.pop('cart')
        return redirect(url_for('main.ordered'))
    return render_template(
        'cart.html',
        cart_items=cart_items,
        cart_amount=cart_amount,
        meals=meals,
        form=form,
    )


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
    orders = Order.query.filter_by(client_email=current_user.email).all()
    return render_template('account.html', orders=orders)


@main_bp.route('/ordered')
def ordered():
    return render_template('ordered.html')
