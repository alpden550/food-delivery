from sqlalchemy import event
from sqlalchemy_utils import EmailType
from werkzeug.security import check_password_hash, generate_password_hash

from food_delivery.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    meals = db.relationship('Meal', back_populates='category', lazy='joined')

    def __repr__(self):
        return f'<Category {self.title}>'


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400))
    picture = db.Column(db.String(100))
    price = db.Column(db.Float())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='meals', lazy='joined')

    def __repr__(self):
        return f'<Meal {self.title}>'


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, *args):  # noqa:WPS110
    return generate_password_hash(value)
