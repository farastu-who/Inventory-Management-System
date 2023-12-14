from flask import Blueprint, request, jsonify
from db import db
from models.supplier import Supplier

supplier_bp = Blueprint('supplier_bp', __name__)

@supplier_bp.route('/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    try:
        new_supplier = Supplier(
            supplier_id=data['supplier_id'],
            supplier_name=data['supplier_name'],
            contact_info=data['contact_info'],
            rating=data['rating']
        )
        db.session.add(new_supplier)
        db.session.commit()
        return jsonify({"message": "Supplier created", "supplier_id": new_supplier.supplier_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@supplier_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    suppliers_data = [{
        'supplier_id': supplier.supplier_id,
        'supplier_name': supplier.supplier_name,
        'contact_info': supplier.contact_info,
        'rating': supplier.rating
    } for supplier in suppliers]
    return jsonify(suppliers_data), 200

@supplier_bp.route('/suppliers/<supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        supplier_data = {
            'supplier_id': supplier.supplier_id,
            'supplier_name': supplier.supplier_name,
            'contact_info': supplier.contact_info,
            'rating': supplier.rating
        }
        return jsonify(supplier_data), 200
    else:
        return jsonify({"message": "Supplier not found"}), 404

@supplier_bp.route('/suppliers/<supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404

    data = request.get_json()
    try:
        supplier.supplier_name = data.get('supplier_name', supplier.supplier_name)
        supplier.contact_info = data.get('contact_info', supplier.contact_info)
        supplier.rating = data.get('rating', supplier.rating)
        db.session.commit()
        return jsonify({"message": "Supplier updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@supplier_bp.route('/suppliers/<supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404

    try:
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({"message": "Supplier deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
