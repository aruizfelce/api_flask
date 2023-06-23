import os
from dotenv import load_dotenv

load_dotenv()

ENVIROMENT = os.getenv('ENVIROMENT')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1213456789-pst-api@localhost:3307/flaskmysql'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://"+DB_USER+":"+DB_PASS+"@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://"+DB_USER+":"+DB_PASS+"@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
