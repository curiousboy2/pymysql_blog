from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Required,Length

class Register_form(Form):
    username=StringField('账号',validators=[Required()])
    password=PasswordField('密码',validators=[Required(),Length(6,8)])
    submit=SubmitField('Register')

class Login_form(Form):
    username=StringField('账号',validators=[Required()])
    password=PasswordField('密码',validators=[Required(),Length(6,8)])
    submit=SubmitField('login')