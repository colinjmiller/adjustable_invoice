from wtforms import Form, StringField, PasswordField, validators


class UserForm(Form):
    email = StringField('email', [validators.Email()])
    password = PasswordField('password')
