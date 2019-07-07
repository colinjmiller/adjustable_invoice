from wtforms import Form, StringField, PasswordField, validators, IntegerField
from wtforms import FloatField


class UserForm(Form):
    email = StringField('email', [validators.Email()])
    password = PasswordField('password')


class InvoiceCreationForm(Form):
    name = StringField('name')


class AddLineItemForm(Form):
    line_item_id = IntegerField('line_item_id')


class EditLineItemAdjustmentForm(Form):
    line_item_id = IntegerField('line_item_id')
    adjustments = FloatField('adjustments')


class LineItemCommentForm(Form):
    message = StringField('message')
