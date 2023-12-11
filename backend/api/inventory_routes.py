from flask import Blueprint, request, jsonify
from app import db
from models.inventory import Inventory

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory_item():
    data = request.json
    try:
        new_item = Inventory(
            item_name=data['item_name'],
            cost=data['cost'],
            stock_level=data['stock_level'],
            supplier_id=data['supplier_id'],
            low_stock_flag=data['low_stock_flag']
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Inventory item added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        inventory_items = Inventory.query.all()
        return jsonify([item.serialize() for item in inventory_items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    try:
        item = Inventory.query.get(item_id)
        if item:
            return jsonify(item.serialize()), 200
        else:
            return jsonify({"message": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    data = request.json
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    try:
        item.item_name = data.get('item_name', item.item_name)
        item.cost = data.get('cost', item.cost)
        item.stock_level = data.get('stock_level', item.stock_level)
        item.supplier_id = data.get('supplier_id', item.supplier_id)
        item.low_stock_flag = data.get('low_stock_flag', item.low_stock_flag)
        db.session.commit()
        return jsonify({"message": "Inventory item updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    try:
        item = Inventory.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Inventory item deleted"}), 200
        else:
            return jsonify({"message": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
