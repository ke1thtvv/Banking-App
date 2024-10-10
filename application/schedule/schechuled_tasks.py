from datetime import datetime
from ..models.models import db, Transfer,  Account, Transaction



def process_transfer(transfer):
    
    # Get accounts
    from_account = Account.query.get(transfer.from_account_id)
    to_account = Account.query.get(transfer.to_account_id)

    # Check if accounts are valid
    if from_account and to_account:
        if from_account.bank_id != to_account.bank_id:
            # Transfer between different banks
            if transfer.status == 'waiting':
                to_account.balance += transfer.amount
                transfer.status = 'completed'
                
                db.session.commit()
            else:
                transfer.status = 'failed'
                db.session.commit()
        else:
            transfer.status = 'invalid'
            db.session.commit()

    if transfer.status != 'completed':
        from_account.balance += transfer.amount
        transfer.status = 'failed'
        db.session.rollback()


        db.session.commit()