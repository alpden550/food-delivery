from flask import flash, redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class Forbidden():
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('Нужен аккаунт администратора!', 'danger')
        return redirect(url_for('auth.login'))


class UserView(Forbidden, ModelView):
    column_exclude_list = ('password',)
    column_labels = {
        'username': 'Юзернейм',
        'email': 'Почта',
        'is_admin': 'Администратор',
        'password': 'Пароль',
    }
    create_modal = True
    edit_modal = True


class AdminDashboard(Forbidden, AdminIndexView):

    @expose('/')
    def index(self):
        return self.render('admin_dashboard.html')
