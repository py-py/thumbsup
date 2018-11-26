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

from app.proxy import proxy_bp
app.register_blueprint(proxy_bp, url_prefix='/proxy')

from app.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, models