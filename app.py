from flask import Flask, jsonify, request, abort
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'db',
    'user': 'root',
    'password': 'root',
    'database': 'db_api'
}

# Establish a connection to the database
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()


# Dummy API key for demonstration purposes
API_KEY = "your_api_key_here"


# Decorator function to check for the presence of the API key in the request headers
def require_api_key(view_function):
    def decorated(*args, **kwargs):
        if 'X-API-Key' not in request.headers or request.headers['X-API-Key'] != API_KEY:
            abort(401)  # Unauthorized
        return view_function(*args, **kwargs)
    return decorated


# Endpoint to add a new customer
@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    query = "INSERT INTO customers (name, email) VALUES (%s, %s)"
    values = (data['name'], data['email'])
    db_cursor.execute(query, values)
    db_connection.commit()

    customer_id = db_cursor.lastrowid
    customer = {
        'id': customer_id,
        'name': data['name'],
        'email': data['email']
    }
    return jsonify(customer), 201


# Endpoint to get all customers
@app.route('/api/customers', methods=['GET'])
def get_customers():
    db_cursor.execute("SELECT * FROM customers")
    customers = [{
        'id': row[0],
        'name': row[1],
        'email': row[2]
    } for row in db_cursor.fetchall()]
    return jsonify(customers), 200


# Endpoint to add a contact for a specific customer
@app.route('/api/customers/<int:customer_id>/contacts', methods=['POST'])
def add_contact(customer_id):
    customer = next((c for c in get_customers()[0] if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    query = "INSERT INTO contacts (customer_id, name, phone) VALUES (%s, %s, %s)"
    values = (customer_id, data['name'], data['phone'])
    db_cursor.execute(query, values)
    db_connection.commit()

    contact_id = db_cursor.lastrowid
    contact = {
        'id': contact_id,
        'customer_id': customer_id,
        'name': data['name'],
        'phone': data['phone']
    }
    return jsonify(contact), 201


# Endpoint to get all contacts for a specific customer
@app.route('/api/customers/<int:customer_id>/contacts', methods=['GET'])
def get_contacts(customer_id):
    db_cursor.execute("SELECT * FROM contacts WHERE customer_id=%s", (customer_id,))
    customer_contacts = [{
        'id': row[0],
        'customer_id': row[1],
        'name': row[2],
        'phone': row[3]
    } for row in db_cursor.fetchall()]

    if not customer_contacts:
        return jsonify({'error': 'No contacts found for this customer'}), 404

    return jsonify(customer_contacts), 200


# Endpoint to add an order for a specific customer
@app.route('/api/customers/<int:customer_id>/orders', methods=['POST'])
def add_order(customer_id):
    customer = next((c for c in get_customers()[0] if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    query = "INSERT INTO orders (customer_id, product, quantity, price) VALUES (%s, %s, %s, %s)"
    values = (customer_id, data['product'], data['quantity'], data['price'])
    db_cursor.execute(query, values)
    db_connection.commit()

    order_id = db_cursor.lastrowid
    order = {
        'id': order_id,
        'customer_id': customer_id,
        'product': data['product'],
        'quantity': data['quantity'],
        'price': data['price']
    }
    return jsonify(order), 201


# Endpoint to get all orders for a specific customer
@app.route('/api/customers/<int:customer_id>/orders', methods=['GET'])
def get_orders(customer_id):
    db_cursor.execute("SELECT * FROM orders WHERE customer_id=%s", (customer_id,))
    customer_orders = [{
        'id': row[0],
        'customer_id': row[1],
        'product': row[2],
        'quantity': row[3],
        'price': row[4]
    } for row in db_cursor.fetchall()]

    if not customer_orders:
        return jsonify({'error': 'No orders found for this customer'}), 404

    return jsonify(customer_orders), 200


if __name__ == '__main__':
    app.run(debug=True)
