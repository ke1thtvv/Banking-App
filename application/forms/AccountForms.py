from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class AddAccountForm(FlaskForm):
    name = StringField('Name of account', validators=[DataRequired(), Length(min=2, max=60)])
    description = TextAreaField('Description')
    bank_id = SelectField('Bank', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditAccountForm(FlaskForm):
    name = StringField('Name of account', validators=[DataRequired(), Length(min=2, max=60)])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')
    