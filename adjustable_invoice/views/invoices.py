from flask import Blueprint, render_template

blueprint = Blueprint('invoices', __name__)


@blueprint.route('/')
def index():
    return render_template('invoices/index.html')
