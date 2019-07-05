from flask import Blueprint, render_template, request
from adjustable_invoice.svc.users.api import UsersAPI

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
def index():
    return render_template('home/index.html')


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('home/signup.html')
    else:
        user = UsersAPI.create_user('testing@example.com', 'password')
        return str(user)
