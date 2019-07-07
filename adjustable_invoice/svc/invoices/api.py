from adjustable_invoice.svc.base import session_scope
from adjustable_invoice.svc.invoices.models import Invoice, LineItem
from adjustable_invoice.svc.invoices.models import LineItemComment
from adjustable_invoice.svc.invoices.exceptions import InvoiceNotFound
from adjustable_invoice.svc.invoices.exceptions import LineItemNotFound
from flask_login import current_user


class InvoicesAPI():

    def invoice_to_dict(invoice):
        return {
            'id': invoice.id,
            'name': invoice.name
        }

    def invoices_to_list(invoices):
        invoice_list = []
        for invoice in invoices:
            invoice_list.append(InvoicesAPI.invoice_to_dict(invoice))
        return invoice_list

    def line_item_to_dict(line_item):
        return {
            'id': line_item.id,
            'invoice_id': line_item.invoice_id,
            'campaign_id': line_item.campaign_id,
            'campaign_name': line_item.campaign_name,
            'line_item_name': line_item.line_item_name,
            'booked_amount': line_item.booked_amount,
            'actual_amount': line_item.actual_amount,
            'adjustments': line_item.adjustments
        }

    def line_items_to_list(line_items):
        line_items_list = []
        for line_item in line_items:
            line_items_list.append(InvoicesAPI.line_item_to_dict(line_item))
        return line_items_list

    def comment_to_dict(comment):
        return {
            'id': comment.id,
            'line_item_id': comment.line_item_id,
            'message': comment.message,
            'owner': comment.owner,
            'created_at': comment.created_at
        }

    def comments_to_list(comments):
        comments_list = []
        for comment in comments:
            comments_list.append(InvoicesAPI.comment_to_dict(comment))
        return comments_list

    def get_invoices_for_user(user_id):
        with session_scope() as session:
            invoices = (
                session.query(Invoice)
                .filter_by(user_id=user_id)
            )
            return InvoicesAPI.invoices_to_list(invoices)

    def create_invoice(invoice_name):
        with session_scope() as session:
            invoice = Invoice()
            invoice.user_id = current_user.get_id()
            invoice.name = invoice_name
            session.add(invoice)

    def get_invoice_by_id(invoice_id):
        with session_scope() as session:
            invoice = (
                session.query(Invoice)
                .filter_by(id=invoice_id)
                .first()
            )

            if not invoice:
                raise InvoiceNotFound('That invoice does not exist')
            return InvoicesAPI.invoice_to_dict(invoice)

    def get_line_item_by_id(line_item_id):
        with session_scope() as session:
            line_item = (
                session.query(LineItem)
                .filter_by(id=line_item_id)
                .first()
            )

            if not line_item:
                raise LineItemNotFound('That line item does not exist')

            return InvoicesAPI.line_item_to_dict(line_item)

    def get_line_items_on_invoice(invoice_id):
        with session_scope() as session:
            line_items = (
                session.query(LineItem)
                .filter_by(invoice_id=invoice_id)
            )

            return InvoicesAPI.line_items_to_list(line_items)

    def get_available_line_items(invoice_id, page):
        PAGE_SIZE = 15
        with session_scope() as session:
            line_items = (
                session.query(LineItem)
                .filter(LineItem.invoice_id.is_(None))
                .offset(page * PAGE_SIZE)
                .limit(PAGE_SIZE)
            )

            return InvoicesAPI.line_items_to_list(line_items)

    def add_line_item_to_invoice(invoice_id, line_item_id):
        with session_scope() as session:
            line_item = (
                session.query(LineItem)
                .filter_by(id=line_item_id)
                .first()
            )
            line_item.invoice_id = invoice_id
            session.add(line_item)

    def set_line_item_adjustment(line_item_id, adjustments):
        with session_scope() as session:
            line_item = (
                session.query(LineItem)
                .filter_by(id=line_item_id)
                .first()
            )

            if not line_item:
                raise LineItemNotFound('That line item does not exist')

            line_item.adjustments = adjustments

            return InvoicesAPI.line_item_to_dict(line_item)

    def get_comments_for_line_item(line_item_id):
        with session_scope() as session:
            comments = (
                session.query(LineItemComment)
                .filter_by(line_item_id=line_item_id)
                .order_by(LineItemComment.created_at.desc())
            )

            return InvoicesAPI.comments_to_list(comments)

    def create_comment_for_line_item(line_item_id, message, owner):
        with session_scope() as session:
            line_item_comment = LineItemComment()
            line_item_comment.line_item_id = line_item_id
            line_item_comment.message = message
            line_item_comment.owner = owner
            session.add(line_item_comment)

    def bulk_add_line_items(line_items):
        with session_scope() as session:
            objects = []
            for line_item in line_items:
                objects.append(LineItem(
                    campaign_id=line_item['campaign_id'],
                    campaign_name=line_item['campaign_name'],
                    line_item_name=line_item['line_item_name'],
                    booked_amount=line_item['booked_amount'],
                    actual_amount=line_item['actual_amount'],
                    adjustments=line_item['adjustments']
                ))
            session.bulk_save_objects(objects)
