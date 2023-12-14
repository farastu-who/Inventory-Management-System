from flask import Blueprint, request, jsonify, render_template
from db import db
from models.order import Order
from datetime import datetime

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        new_order = Order(
            supplier_id=data['supplier_id'],
            item_id=data['item_id'],
            quantity=data['quantity'],
            date=datetime.strptime(data['date'], '%m/%d/%y').date()  # Parse the date from string
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order created", "order_id": new_order.order_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        return render_template('orders.html', orders=orders)
    except Exception as e:
        return render_template('error.html', error=str(e)) 


@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order_data = {
            'order_id': order.order_id,
            'supplier_id': order.supplier_id,
            'item_id': order.item_id,
            'quantity': order.quantity,
            'date': order.date.strftime('%m/%d/%y')
        }
        return jsonify(order_data), 200
    else:
        return jsonify({"message": "Order not found"}), 404
