from flask import Blueprint, flash, redirect, render_template, request, url_for

from food_delivery.form import LoginForm
from food_delivery.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.validate_password(form.password.data):
            flash('Неверное имя пользователя или пароль', 'danger')
            return redirect(url_for('auth.login'))
        return redirect(url_for('main.account'))
    return render_template('auth.html', form=form)
