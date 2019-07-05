from flask import Blueprint, render_template
from flask_login import login_required, current_user
from adjustable_invoice.svc.invoices.api import InvoicesAPI

blueprint = Blueprint('invoices', __name__)


@blueprint.route('/')
@login_required
def index():
    invoices = InvoicesAPI.get_invoices_for_user(current_user.get_id())
    return render_template('invoices/index.html', invoices=invoices)


@blueprint.route('/create')
@login_required
def create():
    return 'OK'
