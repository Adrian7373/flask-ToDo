from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Adriangwapo@localhost:5432/FlaskMarket"
app.config["SECRET_KEY"] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
login_manager.login_message = "Please Log In first"
from ToDo import routes


