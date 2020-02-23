from collections import namedtuple

import pytest
from wtforms.validators import ValidationError

from food_delivery.validators import (
    has_digit,
    has_letters,
    has_special_symbols,
    has_upper_letters,
    password_is_long,
    validate_phone,
)


@pytest.fixture
def field():
    Field = namedtuple('field', ['data'])
    field = Field('')
    yield field


class TestValidators:

    def test_validate_phone(self, field):
        new_field = field._replace(data='1234567890')
        with pytest.raises(ValidationError):
            validate_phone('form', new_field)

    def test_password_is_long(self, field):
        new_field = field._replace(data='12345')
        with pytest.raises(ValidationError):
            password_is_long('form', new_field)

    def test_has_upper_letters(self, field):
        new_field = field._replace(data='qwerty')
        with pytest.raises(ValidationError):
            has_upper_letters('form', new_field)

    def test_has_digit(self, field):
        new_field = field._replace(data='qwerty')
        with pytest.raises(ValidationError):
            has_digit('form', new_field)

    def test_has_letters(self, field):
        new_field = field._replace(data='123456789')
        with pytest.raises(ValidationError):
            has_letters('form', new_field)

    def test_has_special_symbols(self, field):
        new_field = field._replace(data='qwerty123456789')
        with pytest.raises(ValidationError):
            has_special_symbols('form', new_field)
