# Food Delivery

[![Maintainability](https://api.codeclimate.com/v1/badges/8de202229b49d8404911/maintainability)](https://codeclimate.com/github/alpden550/food-delivery/maintainability) [![Build Status](https://travis-ci.org/alpden550/food-delivery.svg?branch=master)](https://travis-ci.org/alpden550/food-delivery) [![Coverage Status](https://coveralls.io/repos/github/alpden550/food-delivery/badge.svg)](https://coveralls.io/github/alpden550/food-delivery)

Flask app for meal delivery service. Include adminpanel too.

[Example hosted on the Heroku](https://stepik-food-delivery.herokuapp.com)

## How to install

Download code or clone it from Github, and install dependencies.

If you have already installed Poetry, type command:

```bash
poetry install --no-dev
```

If not, should use a virtual environment for the best project isolation. Activate venv and install dependencies:

```bash
pip install -r requirements.txt
```

And set environment variables:

```bash
export SECRET_KEY=some extra secret key
export DATABASE_URL="postgresql://@localhost:5432/databasename"
```

## How to run

Before start, should fill database and create superuser, if it needs.

```bash
flask init
flask fill
```

```bash
flask superuser -n admin -p password -e test@mail.ru
```

And start web server:

```bash
flask run
```
