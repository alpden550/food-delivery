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


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, *args):  # noqa:WPS110
    return generate_password_hash(value)
