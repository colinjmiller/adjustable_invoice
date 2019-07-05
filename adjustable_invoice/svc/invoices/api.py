from adjustable_invoice.svc.base import session_scope
from adjustable_invoice.svc.invoices.models import Invoice, LineItem


class InvoicesAPI():

    def invoices_to_list(invoices):
        invoice_list = []
        for invoice in invoices:
            invoice_list.append({
                'id': invoice.id,
                'name': invoice.name
            })
        return invoice_list

    def get_invoices_for_user(user_id):
        with session_scope() as session:
            invoices = (
                session.query(Invoice)
                .filter_by(user_id=user_id)
            )
            return InvoicesAPI.invoices_to_list(invoices)
