from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
  tele_id = StringField('Telegram ID', validators=[DataRequired("Please enter your telegram ID.")])
  tele_hash = StringField('Telegram Hash', validators=[DataRequired("Please enter your telegram Hash")])
  tele_channel = StringField('Telegram channel name', validators=[DataRequired("Please enter your telegram channel name")])
  accountid = StringField('3commas Account ID', validators=[DataRequired("Please enter your 3commas account id")])
  accountkey = StringField('3commas Account API KEY', validators=[DataRequired("Please enter your 3commas account API KEY")])
  accountsecret = StringField('3commas Account API Secret', validators=[DataRequired("Please enter your 3commas account API Secret")])
  submit = SubmitField('Trade')
