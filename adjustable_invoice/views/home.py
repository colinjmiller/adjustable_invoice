from flask import Blueprint, render_template, request, redirect, flash, url_for
from .forms import UserForm
from adjustable_invoice.svc.users import exceptions
from adjustable_invoice.svc.users.api import UsersAPI
from flask_login import login_user, logout_user, current_user

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('invoices.index'))
    return render_template('home/index.html')


@blueprint.route('/login', methods=['POST'])
def login():
    form = UserForm(request.form)
    if not form.validate():
        return _handle_invalid_form(form, url_for('home.index'))

    try:
        user = UsersAPI.authenticate_user(form.email.data, form.password.data)
    except exceptions.AuthenticationFailed as e:
        flash(e.value, 'error')
        return redirect(url_for('home.index'))

    login_user(UsersAPI.get_user_by_id(user['id']))
    return redirect(url_for('invoices.index'))


@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('home/signup.html')

    # This is a POST request; handle signup request
    # 1. Validate the input
    form = UserForm(request.form)
    if not form.validate():
        return _handle_invalid_form(form, url_for('home.signup'))

    # 2. Create the user
    try:
        user = UsersAPI.create_user(form.email.data, form.password.data)
    except exceptions.UserAlreadyExists as e:
        flash(e.value, 'error')
        return redirect(url_for('home.signup'))

    login_user(UsersAPI.get_user_by_email(user['email']))
    return redirect(url_for('invoices.index'))


def _handle_invalid_form(form, redirect_location):
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            flash(err, 'error')
    return redirect(redirect_location)
