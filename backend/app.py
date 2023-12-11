from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.api.inventory_routes import inventory_blueprint
from backend.api.order_routes import orders_blueprint
from backend.api.supplier_routes import suppliers_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'  # Using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register blueprints
app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
app.register_blueprint(orders_blueprint, url_prefix='/order')
app.register_blueprint(suppliers_blueprint, url_prefix='/supplier')


db = SQLAlchemy(app)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
