from ..models.models import Account, Bank, db
from ..forms.AccountForms import AddAccountForm, EditAccountForm
from flask import Blueprint
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_login import LoginManager,  login_user, login_required, logout_user, current_user
from .auth import role_required

account = Blueprint('account', __name__)

@login_required
@account.route('/accounts', methods =['GET'])
def show_user_accounts():
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    return render_template('user_accounts.html', accounts = accounts)

@login_required
@account.route('/account/<account_id>', methods =['GET'])
def show_account(account_id):
    account = Account.query.get_or_404(id = account_id)
    return render_template('single_account.html', account = account)

@login_required
@account.route('/add_account', methods = ['GET', 'POST'])
def add_bank_account():
    form = AddAccountForm()

    banks = Bank.query.all()
    form.bank_id.choices = [(bank.id, bank.name) for bank in banks]

    if form.validate_on_submit():
        account = Account(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            balance=0,
            bank_id=form.bank_id.data
        )
        db.session.add(account)
        db.session.commit()
        flash("You created new bank account!")
        return redirect(url_for('account.show_user_accounts'))
    return render_template('add_account.html', form = form)

@login_required
@account.route('/edit_account/<id_to_edit>', methods= ['GET', 'POST'])
def edit_account(id_to_edit):
    account = Account.query.get_or_404(id_to_edit)

    if(account.user_id != current_user.id and current_user.role != 'admin'):
        abort(403)
    form = EditAccountForm(obj = account)

    if form.validate_on_submit():
        account.name = form.name.data
        account.description = form.description.data
        db.session.commit()
        return redirect(url_for('account.show_user_accounts'))
    return render_template('edit_account.html', form = form)

