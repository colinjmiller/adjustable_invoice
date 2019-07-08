from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from adjustable_invoice.svc.invoices.api import InvoicesAPI
from adjustable_invoice.svc.invoices.exceptions import InvoiceNotFound
from adjustable_invoice.svc.invoices.exceptions import LineItemNotFound
from .forms import InvoiceCreationForm, AddLineItemForm
from .forms import EditLineItemAdjustmentForm, LineItemCommentForm

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


@blueprint.route('/edit_line_item/<int:line_item_id>', methods=['GET'])
@login_required
def edit_line_item(line_item_id):
    try:
        line_item = InvoicesAPI.get_line_item_by_id(line_item_id)
        comments = InvoicesAPI.get_comments_for_line_item(line_item_id)
    except LineItemNotFound as e:
        flash(e.value, 'error')
        return redirect(url_for('invoices.index'))

    return render_template('invoices/edit_line_item.html',
                           line_item=line_item,
                           comments=comments)


@blueprint.route('/edit_line_item_adjustment/<int:line_item_id>',
                 methods=['POST'])
@login_required
def edit_line_item_adjustment(line_item_id):
    form = EditLineItemAdjustmentForm(request.form)
    if not form.validate():
        flash('Could not edit that line item adjustment', 'error')
        return redirect(url_for('invoices.edit_line_item',
                                line_item_id=line_item_id))
    try:
        InvoicesAPI.set_line_item_adjustment(line_item_id,
                                             form.adjustments.data)
    except LineItemNotFound as e:
        flash(e.value, 'error')
        return redirect(url_for('invoices.index'))

    return redirect(url_for('invoices.edit_line_item',
                            line_item_id=line_item_id))


@blueprint.route('/edit_line_item/<int:line_item_id>/comment',
                 methods=['POST'])
@login_required
def comment_on_line_item(line_item_id):
    form = LineItemCommentForm(request.form)
    if not form.validate():
        flash('Could not add comment', 'error')
        return redirect(url_for('invoices.edit_line_item',
                                line_item_id=line_item_id))

    InvoicesAPI.create_comment_for_line_item(line_item_id,
                                             form.message.data,
                                             current_user.email)

    return redirect(url_for('invoices.edit_line_item',
                            line_item_id=line_item_id))
