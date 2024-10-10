from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..models.models import Account, Transfer, db
from ..forms.TransferForms import TransferForm, TransferHistoryForm
from datetime import datetime, timedelta

transfer = Blueprint('transfer', __name__)

@login_required
@transfer.route('/transfer', methods=['GET', 'POST'])
def transfercash():
    form = TransferForm()
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    form.from_account_id.choices = [(account.id, f'{account.name} ({account.balance} PLN)') for account in accounts]

    if form.validate_on_submit():
        from_account = Account.query.get_or_404(form.from_account_id.data)
        if from_account.user_id != current_user.id:
            abort(403)

        to_account = Account.query.filter_by(id=form.to_account_id.data).first()
        if not to_account:
            flash('Recipient account not found', 'error')
        return render_template('transfer.html', form=form)

        if from_account.balance < form.amount.data:
            flash('Insufficient funds in the account', 'error')
        return render_template('transfer.html', form=form)

        
        if from_account.bank_id == to_account.bank_id:
            # Immediate transfer within the same bank
            new_transfer = Transfer(
                from_account_id=from_account.id,
                to_account_id=to_account.id,
                title=form.title.data,
                amount=form.amount.data,
                status='completed'
            )
            from_account.balance -= form.amount.data
            to_account.balance += form.amount.data
            db.session.add(new_transfer)
            
            db.session.commit()
            flash('Transfer completed successfully', 'success')

        else:
            # Schedule transfer between different banks
            new_transfer = Transfer(
                from_account_id=from_account.id,
                to_account_id=to_account.id,
                title=form.title.data,
                amount=form.amount.data,
                status='waiting'
            )
            from_account.balance -= form.amount.data
            db.session.add(new_transfer)

            db.session.commit()
            flash('The transfer is pending approval', 'info')

        return redirect(url_for('account.show_user_accounts'))

    return render_template('transfer.html', form=form)


@login_required
@transfer.route('/transfer_history', methods=['GET', 'POST'])
def transferhistory():
    form = TransferHistoryForm()
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    form.from_account_id.choices = [(account.id, f'{account.name} ({account.balance} PLN)') for account in accounts]

    if form.validate_on_submit():
        account = Account.query.get_or_404(form.from_account_id.data)
        if account.user_id != current_user.id:
            abort(403)
        incomes = Transfer.query.filter_by(to_account_id=account.id, status='completed').all()
        outcomes = Transfer.query.filter_by(from_account_id=account.id, status='completed').all()
        return render_template('transfer_history.html', form = form, incomes=incomes, outcomes=outcomes)

    return render_template('transfer_history.html', form = form, incomes=[], outcomes=[])