from flask import Flask, render_template
from flask_migrate import Migrate
from flyflask.config import configs
from flyflask.models import db, Env, Mdb, User
from flask_login import LoginManager
from flyflask.handlers import front, env, admin, user


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'

# 注册蓝图


def register_blueprints(app):
    app.register_blueprint(front)
    # 环境蓝图
    app.register_blueprint(env)
    app.register_blueprint(admin)
    app.register_blueprint(user)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprints(app)
    return app
