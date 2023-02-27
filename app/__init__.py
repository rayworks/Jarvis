from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_pagedown import PageDown


from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login.index'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    print(">>> config db : ", config[config_name].SQLALCHEMY_DATABASE_URI)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    #
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .views.main import main_bp
    app.register_blueprint(main_bp)

    from .views.login import login
    app.register_blueprint(login, url_prefix='/login')

    from .views.todo_lists import todo_list
    app.register_blueprint(todo_list, url_prefix='/todo_list')

    return app
