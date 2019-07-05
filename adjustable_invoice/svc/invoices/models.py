from adjustable_invoice.svc.base import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)


class LineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    campaign_id = db.Column(db.Integer)
    campaign_name = db.Column(db.String)
    line_item_name = db.Column(db.String)
    booked_amount = db.Column(db.Float)
    actual_amount = db.Column(db.Float)
    adjustments = db.Column(db.Float)
