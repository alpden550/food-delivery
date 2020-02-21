from food_delivery import create_app
from food_delivery.extensions import db

app = create_app(config_name='testing')
db.create_all(app=app)
