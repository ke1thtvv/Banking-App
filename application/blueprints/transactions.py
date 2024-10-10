from ..models.models import Account, db, Transaction
from ..forms.TransactionForms import DepositForm, DepositFormSec, WithdrawForm, HistoryForm
from flask import Blueprint
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_login import LoginManager,  login_user, login_required, logout_user, current_user
from .auth import role_required

transaction = Blueprint('transaction', __name__)

@login_required
@transaction.route('/choose_account_and_deposit', methods = ['GET', 'POST'])
def atmdeposit():
    form = DepositForm()
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    form.account_id.choices = [(account.id, account.name) for account in accounts]

    if form.validate_on_submit():
        account = Account.query.get_or_404(form.account_id.data)

        if account.user_id != current_user.id:
            abort(403)
        
        new_transaction = Transaction(account_id = account.id, amount = form.amount.data , action = 'deposit')
        db.session.add(new_transaction)
        db.session.commit()
        account.balance = account.balance + new_transaction.amount
        db.session.commit()

        flash(f'Deposited {new_transaction.amount} PLN to your account', 'success')
        return redirect(url_for('account.show_user_accounts'))
    return render_template('deposit.html', form = form)

@login_required
@transaction.route('/simple_deposit/<account_id>', methods = ['GET', 'POST'])
def simpledeposit(account_id):
    form = DepositFormSec()
    account = Account.query.get_or_404(account_id)

    if account.user_id != current_user.id :
            abort(403)

    if form.validate_on_submit():
        new_transaction = Transaction(account_id = account.id, amount = form.amount.data, action = 'deposit')
        db.session.add(new_transaction)
        db.session.commit()
        account.balance = account.balance + new_transaction.amount
        db.session.commit()
        flash('Success!')
        return redirect(url_for('account.show_user_accounts'))
    return render_template('deposit2.html', form = form)


@login_required
@transaction.route('/withdraw/<account_id>', methods = ['GET', 'POST'])
def withdraw(account_id):
    form = WithdrawForm()
    account = Account.query.get_or_404(account_id)

    if account.user_id != current_user.id:
            abort(403)

    form.set_max_amount(account.balance)

    if form.validate_on_submit():
        amount = form.amount.data
        new_transaction = Transaction(account_id = account.id, amount = amount, action = 'withdraw')
        db.session.add(new_transaction)
        db.session.commit()
        account.balance = account.balance - new_transaction.amount
        db.session.commit()
        flash(f"Withdraw {amount} PLN from your account", "success")
        return redirect(url_for('account.show_user_accounts'))
    return render_template('withdraw.html', form = form)

@login_required
@transaction.route('/choose_account_and_withdraw', methods=['GET', 'POST'])
def simple_withdraw():
    form = WithdrawForm()
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    form.account_id.choices = [(account.id, account.name) for account in accounts]

    if form.validate_on_submit():
        account = Account.query.get_or_404(form.account_id.data)

        if account.user_id != current_user.id:
            abort(403)
        
        amount = form.amount.data
        if amount > account.balance:
            flash('Insufficient funds!', 'error')
            return redirect(url_for('transaction.simple_withdraw'))

        new_transaction = Transaction(account_id=account.id, amount=amount, action='withdraw')
        db.session.add(new_transaction)
        account.balance -= amount
        db.session.commit()

        flash(f'Withdrew {amount} PLN from your account', 'success')
        return redirect(url_for('account.show_user_accounts'))

    return render_template('withdraw.html', form=form)

@login_required
@transaction.route('/withdraw_history/<account_id>', methods = ['GET'])
def withdraw_history(account_id):
    account = Account.query.get_or_404(account_id)

    if account.user_id != current_user.id and current_user.role != 'admin':
            abort(403)
    
    withdraws = Transaction.query.filter_by(account_id = account.id).filter_by(action = 'withdraw')

    return render_template('withdraw_history.html', withdraws = withdraws)


@login_required
@transaction.route('/deposit_history/<account_id>', methods = ['GET'])
def deposit_history(account_id):
    account = Account.query.get_or_404(account_id)

    if account.user_id != current_user.id and current_user.role != 'admin':
            abort(403)
    
    deposits = Transaction.query.filter_by(account_id = account.id).filter_by(action = 'deposit')

    return render_template('withdraw_history.html', deposits = deposits)


@login_required
@transaction.route('/transactionss_history/', methods = ['GET', 'POST'])
def transaction_history():
    form=HistoryForm()
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    form.account_id.choices = [(account.id, account.name) for account in accounts]

    if form.validate_on_submit():
        account=Account.query.get_or_404(form.account_id.data)
        transactions = Transaction.query.filter_by(account_id=account.id)
        
        return render_template('withdraw_history.html', withdraws = transactions, form=form)

    return render_template('withdraw_history.html', withdraws = [], form=form)



