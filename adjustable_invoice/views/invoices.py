from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from adjustable_invoice.svc.invoices.api import InvoicesAPI
from adjustable_invoice.svc.invoices.exceptions import InvoiceNotFound
from .forms import InvoiceCreationForm, AddLineItemForm

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


@blueprint.route('/edit_invoice/<int:invoice_id>', methods=['GET'])
@login_required
def edit_invoice(invoice_id):
    try:
        invoice = InvoicesAPI.get_invoice_by_id(invoice_id)
        line_items = InvoicesAPI.get_line_items_on_invoice(invoice_id)
    except InvoiceNotFound as e:
        flash(e.value, 'error')
        return redirect(url_for('invoices.index'))

    return render_template('invoices/edit_invoice.html',
                           invoice=invoice,
                           line_items=line_items)

@blueprint.route('/edit_invoice/<int:invoice_id>/add_line_items/<int:page>')
@login_required
def add_line_items(invoice_id, page):
    if page < 1:
        return redirect(url_for('invoices.add_line_items',
                                invoice_id=invoice_id,
                                page=1))
    line_items = InvoicesAPI.get_available_line_items(invoice_id, page - 1)

    if not line_items:
        flash('There were no more line items to show', 'error')
        return redirect(url_for('invoices.add_line_items',
                                invoice_id=invoice_id,
                                page=1))

    return render_template('invoices/add_line_items.html',
                           invoice_id=invoice_id,
                           line_items=line_items,
                           page=page)

@blueprint.route('/edit_invoice/<int:invoice_id>/add_line_items/<int:page>',
                 methods=['POST'])
@login_required
def add_line_item_to_invoice(invoice_id, page):
    form = AddLineItemForm(request.form)
    if not form.validate():
        flash('We could not add that line item', 'error')
        return redirect(url_for('invoices.edit_invoice',
                        invoice_id=invoice_id))

    InvoicesAPI.add_line_item_to_invoice(invoice_id, form.line_item_id.data)

    return redirect(url_for('invoices.add_line_items',
                            invoice_id=invoice_id,
                            page=page))
