from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data to simulate a database (for simplicity, we use dictionaries)
customers = []
contacts = []
orders = []


# Endpoint to add a new customer
@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer = {
        'id': len(customers) + 1,
        'name': data['name'],
        'email': data['email']
    }
    customers.append(customer)
    return jsonify(customer), 201


# Endpoint to get all customers
@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200


# Endpoint to add a contact for a specific customer
@app.route('/api/customers/<int:customer_id>/contacts', methods=['POST'])
def add_contact(customer_id):
    customer = next((c for c in customers if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    contact = {
        'id': len(contacts) + 1,
        'customer_id': customer_id,
        'name': data['name'],
        'phone': data['phone']
    }
    contacts.append(contact)
    return jsonify(contact), 201


# Endpoint to get all contacts for a specific customer
@app.route('/api/customers/<int:customer_id>/contacts', methods=['GET'])
def get_contacts(customer_id):
    customer_contacts = [c for c in contacts if c['customer_id'] == customer_id]
    if not customer_contacts:
        return jsonify({'error': 'No contacts found for this customer'}), 404
    return jsonify(customer_contacts), 200


# Endpoint to add an order for a specific customer
@app.route('/api/customers/<int:customer_id>/orders', methods=['POST'])
def add_order(customer_id):
    customer = next((c for c in customers if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    order = {
        'id': len(orders) + 1,
        'customer_id': customer_id,
        'product': data['product'],
        'quantity': data['quantity'],
        'price': data['price']
    }
    orders.append(order)
    return jsonify(order), 201


# Endpoint to get all orders for a specific customer
@app.route('/api/customers/<int:customer_id>/orders', methods=['GET'])
def get_orders(customer_id):
    customer_orders = [o for o in orders if o['customer_id'] == customer_id]
    if not customer_orders:
        return jsonify({'error': 'No orders found for this customer'}), 404
    return jsonify(customer_orders), 200


if __name__ == '__main__':
    app.run(debug=True)
