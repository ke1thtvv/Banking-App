from flask_wtf import FlaskForm
from wtforms import  SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class DepositForm(FlaskForm):
    account_id = SelectField('Account', coerce=str, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=1, max=1000000)])
    submit =  SubmitField('Deposit')

class DepositFormSec(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=1, max=1000000)])
    submit =  SubmitField('Deposit')

class WithdrawForm(FlaskForm):
    account_id = SelectField('Account', coerce=str, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=1)])
    submit =  SubmitField('Deposit')

    def set_max_amount(self, max_amount):
        self.amount.validators.append(NumberRange(max=max_amount))

class HistoryForm(FlaskForm):
    account_id = SelectField('Account', coerce=str, validators=[DataRequired()])
    submit =  SubmitField('View history')