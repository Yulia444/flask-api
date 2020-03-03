import os
from dotenv import load_dotenv


load_dotenv()


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')


class DevConfig(Config):
    DEBUG=True


class ProdConfig(Config):
    DEBUG=False
