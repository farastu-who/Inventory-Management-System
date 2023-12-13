from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.api.inventory_routes import inventory_bp
from backend.api.order_routes import orders_bp
from backend.api.supplier_routes import suppliers_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IMS.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Initialize the SQLAlchemy app, after the Flask app is created
db.init_app(app)

# Register blueprints
app.register_blueprint(inventory_bp, url_prefix='/inventory')
app.register_blueprint(orders_bp, url_prefix='/order')
app.register_blueprint(suppliers_bp, url_prefix='/supplier')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
