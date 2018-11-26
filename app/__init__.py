from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'

from app.proxy import proxy
app.register_blueprint(proxy, url_prefix='/proxy')

from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app import routes, models