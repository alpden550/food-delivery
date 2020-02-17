from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()
csrf = CSRFProtect()
login = LoginManager()

login.login_view = 'auth.login'
login.login_message = 'Авторизуйтесь для доступа.'
