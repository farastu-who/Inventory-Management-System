from .inventory import db
from datetime import datetime

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
