from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.LocalConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from .util import assets
from app.models import *
from app.mod_dashboard.controllers import mod_dashboard as dashboard_module
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_admin.controllers import mod_admin as admin_module
from app.mod_api.controllers import mod_api as api_module

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(dashboard_module)
app.register_blueprint(auth_module)
app.register_blueprint(admin_module)
app.register_blueprint(api_module)
db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run()
