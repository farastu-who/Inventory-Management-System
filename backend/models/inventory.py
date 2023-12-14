from flask_sqlalchemy import SQLAlchemy
from db import db

class Inventory(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.String(50), nullable=False)
    low_stock_flag = db.Column(db.String(3))  # 'Yes' or 'No'

    def serialize(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "cost": self.cost,
            "stock_level": self.stock_level,
            "supplier_id": self.supplier_id,
            "low_stock_flag": self.low_stock_flag
        }
