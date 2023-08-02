-- Create the 'customers' table
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Create the 'contacts' table
CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Create the 'orders' table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Insert some initial data (optional)
INSERT INTO customers (name, email) VALUES
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com');

INSERT INTO contacts (customer_id, name, phone) VALUES
    (1, 'John Doe Contact', '123-456-7890'),
    (2, 'Jane Smith Contact', '987-654-3210');

INSERT INTO orders (customer_id, product, quantity, price) VALUES
    (1, 'Product A', 3, 29.99),
    (2, 'Product B', 2, 19.99);
