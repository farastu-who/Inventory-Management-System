from .inventory import db

class Supplier(db.Model):
    supplier_id = db.Column(db.String(50), primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
