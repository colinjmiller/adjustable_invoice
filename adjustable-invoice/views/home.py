from flask import Blueprint, render_template, request
# from .svc.users.api import UsersAPI

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
def index():
    return render_template('home/index.html')


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('home/signup.html')
    else:
        return 'OK'
