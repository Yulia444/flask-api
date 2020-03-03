from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from flask.helpers import get_debug_flag
from app.config import DevConfig, ProdConfig


app = Flask(__name__)

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app.config.from_object(CONFIG)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager(app)
db.init_app(app)
migrate.init_app(app, db)


from app import views
from app.models import Event, Participants, Enrollments, Locations
from app.admin import admin