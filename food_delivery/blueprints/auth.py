from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_

from food_delivery.extensions import db
from food_delivery.form import LoginForm, RegistrationForm
from food_delivery.models import User
from food_delivery.utils import check_cart

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login/', methods=('GET', 'POST'))
def login():
    cart = check_cart()

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.validate_password(form.password.data):
            flash('Неверное имя пользователя или пароль', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remembered.data)
        return redirect(url_for('main.index'))
    return render_template('auth.html', form=form, cart=cart)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Разлогинили!', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/registration/', methods=('GET', 'POST'))
def registration():
    cart = check_cart()

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter(  # noqa:WPS337
            or_(User.email == form.email.data, User.username == form.username.data),
        ).first():
            flash('Такой пользователь уже существует.', 'danger')
            return render_template('registration.html', form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Успешно! Теперь можно зайти.', 'success')
        return redirect(url_for('auth.login'))

    return render_template(
        'registration.html',
        form=form,
        cart=cart,
    )
