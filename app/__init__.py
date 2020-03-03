from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager(app)
db.init_app(app)
migrate.init_app(app, db)


from app import views
from app.models import Event, Participants, Enrollments, Locations
from app.admin import admin