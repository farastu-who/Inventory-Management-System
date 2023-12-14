from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import db  
from api.inventory_routes import inventory_bp
from api.order_routes import order_bp
from api.supplier_routes import supplier_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IMS.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(order_bp, url_prefix='/order')
    app.register_blueprint(supplier_bp, url_prefix='/supplier')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
