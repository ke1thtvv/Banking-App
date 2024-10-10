from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,  login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.models import db, User
from ..forms.AuthForms import LoginForm, RegisterForm
from flask import Blueprint
from functools import wraps

auth = Blueprint('auth', __name__)

@auth.route('/')
def welcome():
    return render_template('welcome.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.role == 'admin':
                return 'ok'  #Zrób przekierowanie
            return redirect(url_for('account.show_user_accounts'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form) #template


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email = form.email.data,name=form.name.data, surname=form.surname.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
            
    return render_template('register.html', form=form) #template


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return func(*args, **kwargs)
        return decorated_view
    return decorator
