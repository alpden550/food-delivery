from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from food_delivery.form import LoginForm
from food_delivery.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login/', methods=('GET', 'POST'))
def login():
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
    return render_template('auth.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Разлогинили!', 'info')
    return redirect(url_for('main.index'))

# TODO: Add registration

# TODO: Add reset password
