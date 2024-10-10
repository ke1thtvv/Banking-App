from datetime import timedelta
from flask_login import LoginManager
from flask import Flask
from ..blueprints.auth import auth
from ..blueprints.account import account
from ..blueprints.transactions import transaction
from ..blueprints.transfer import transfer
from ..models.models import db, create_initial_data, User

def config(app, db):
    app.config['SECRET_KEY'] = 'twoj_tajny_klucz' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
    db.init_app(app)

def loginManeger(app):
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    return login_manager

def create_app():
    app = Flask(__name__, template_folder='templates')
    config(app=app, db=db)

    login_manager = loginManeger(app)

    app.register_blueprint(auth)
    app.register_blueprint(account)
    app.register_blueprint(transaction)
    app.register_blueprint(transfer)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()
        create_initial_data()

    return app