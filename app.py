from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_code TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert sample data (run once)
def insert_sample_data():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    sample_data = [
        ('A101', 150.50, 25, 'Shelf 1'),
        ('B202', 200.00, 15, 'Shelf 2'),
        ('C303', 120.75, 50, 'Shelf 3'),
    ]
    cursor.executemany('INSERT INTO products (category_code, price, quantity, location) VALUES (?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

# API Endpoint: Search Product by Category Code
@app.route('/search', methods=['POST'])
def search_product():
    category_code = request.json.get('category_code', '').strip()
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT price, quantity, location FROM products WHERE category_code = ?', (category_code,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return jsonify({
            'price': product[0],
            'quantity': product[1],
            'location': product[2]
        })
    else:
        return jsonify({'error': 'Category code not found.'}), 404

# Web Interface: Inventory Page
@app.route('/inventory')
def inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('inventory.html', products=products)

# Main Home Page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    # Uncomment the line below to populate the database with sample data
    # insert_sample_data()
    app.run(debug=True)
