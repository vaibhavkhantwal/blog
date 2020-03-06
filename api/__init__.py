from flask import Flask
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql+psycopg2://postgres:123456@localhost:5433/postgres"
app.config['SECRET_KEY']="ApiTesting"
db=SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
from api.blueprint import bp 

app.register_blueprint(bp)