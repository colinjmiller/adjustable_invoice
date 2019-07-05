from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from adjustable_invoice.svc.invoices.api import InvoicesAPI
from .forms import InvoiceCreationForm

blueprint = Blueprint('invoices', __name__)


@blueprint.route('/')
@login_required
def index():
    invoices = InvoicesAPI.get_invoices_for_user(current_user.get_id())
    return render_template('invoices/index.html', invoices=invoices)


@blueprint.route('/new_invoice', methods=['GET', 'POST'])
@login_required
def new_invoice():
    if request.method == 'GET':
        return render_template('invoices/new_invoice.html')

    form = InvoiceCreationForm(request.form)
    if not form.validate():
        flash('Invalid invoice creation request', 'error')
        return redirect(url_for('invoices.index'))

    InvoicesAPI.create_invoice(form.name.data)
    return redirect(url_for('invoices.index'))
