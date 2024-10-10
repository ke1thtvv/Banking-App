from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import uuid
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=True)
    surname = db.Column(db.String(64), unique=False, nullable=True)
    email = db.Column(db.String(320), index=True, unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    accounts = db.relationship('Account', backref='owner', lazy=True)
    role = db.Column(db.String(20), nullable=False, default='user')
    
    def set_password(self, password):
        self.password_hash =  generate_password_hash(password, salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Account(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda:(str)(uuid.uuid4().int))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(60), nullable = False)
    description = db.Column(db.String(300))
    balance = db.Column(db.Float, nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)
    bank = db.relationship('Bank', back_populates='accounts')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    action = db.Column(db.String(10), nullable = False)

class Transfer(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=lambda:uuid.uuid4().hex)
    from_account_id = db.Column(db.String, db.ForeignKey('account.id'), nullable=False)
    to_account_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String(60), nullable = False, default= 'Transfer')
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(20), nullable=False, default='waiting')

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable = False, default= 'Transfer')
    accounts = db.relationship('Account', back_populates='bank')




def create_initial_data():
    # Sprawdź, czy istnieją już banki i użytkownicy, a jeśli nie, utwórz nowe rekordy

    # Sprawdź banki
    banks = Bank.query.all()
    if not banks:
        # Tworzenie 3 banków, jeśli nie istnieją
        bank1 = Bank(name='Bank A')
        bank2 = Bank(name='Bank B')
        bank3 = Bank(name='Bank C')

        db.session.add_all([bank1, bank2, bank3])
        db.session.commit()
        print("Dodano 3 banki do bazy danych.")
    else:
        print("Banki już istnieją w bazie danych.")

    # Sprawdź użytkowników
    admin_user = User.query.filter_by(name='admin').first()
    normal_user = User.query.filter_by(name='user').first()
    
    if not admin_user:
        # Utwórz użytkownika admin, jeśli nie istnieje
        admin_user = User(email='admin@example.com',name = 'admin', surname = 'admin', role='admin')
        admin_user.set_password('adminpassword')  # Ustaw hasło użytkownika admin
        db.session.add(admin_user)
        db.session.commit()
        print("Utworzono użytkownika 'admin'.")
    else:
        print("Użytkownik 'admin' już istnieje.")

    if not normal_user:
        # Utwórz użytkownika normalnego, jeśli nie istnieje
        normal_user = User(name = 'user', surname = 'user', email='user@example.com')
        normal_user.set_password('userpassword')  # Ustaw hasło użytkownika normalnego
        db.session.add(normal_user)
        db.session.commit()
        print("Utworzono użytkownika 'user'.")
    else:
        print("Użytkownik 'user' już istnieje.")
