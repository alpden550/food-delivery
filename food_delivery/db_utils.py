import csv

import click
from sqlalchemy.exc import IntegrityError

from food_delivery.extensions import db
from food_delivery.models import Category, Meal


def create_categories(name):
    category = Category(title=name)
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    else:
        click.echo(f'Added Category {name.capitalize()}')


def create_meals(meal_data):
    category = Category.query.filter(
        Category.title == meal_data.get('category'),
    ).first()
    meal = Meal(
        title=meal_data.get('title'),
        description=meal_data.get('description'),
        picture=meal_data.get('picture'),
        price=meal_data.get('price'),
        category=category,
    )
    db.session.add(meal)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    else:
        click.echo(f'Aded meal {meal.title} from category {meal.category}')


def fill_db(meal_csv='meals.csv'):
    meals = []
    with open(meal_csv) as csv_fiile:
        meals_data = csv.DictReader(csv_fiile, delimiter=',')
        for meal in meals_data:
            meals.append(meal)

    categories = {meal['category'] for meal in meals}
    for category in categories:
        create_categories(category)
    for meal_data in meals:
        create_meals(meal_data)


if __name__ == '__main__':
    fill_db()
