from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class TransferForm(FlaskForm):
    recipient_name = StringField('Recipient Name', validators=[DataRequired()])
    from_account_id = SelectField('From Account', coerce=str, validators=[DataRequired()])
    to_account_id = StringField('To Account', validators=[DataRequired()])
    optional_address = TextAreaField('Add Address (optional)')
    amount = FloatField('Transfer Amount', validators=[DataRequired(), NumberRange(min=1)])
    title = StringField('Transfer Title', validators=[DataRequired()])
    submit = SubmitField('Submit Transfer')

class TransferHistoryForm(FlaskForm):
    from_account_id = SelectField('From Account', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Show transfers')