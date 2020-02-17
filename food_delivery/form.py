import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import ValidationError


def validate_phone(form, field):
    try:  # noqa:WPS229
        phone = phonenumbers.parse(field.data, 'RU')
        if not phonenumbers.is_valid_number(phone):
            raise ValueError()
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError('Введите ваш номер, с 8 или без.')


class OrderForm(FlaskForm):
    name = StringField(label='Ваше имя')
    address = StringField(label='Адрес')
    email = EmailField(label='Электропочта')
    phone = TelField('Телефон', validators=[validate_phone])
