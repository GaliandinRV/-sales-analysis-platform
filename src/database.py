import sqlite3 as sql
def get_connection():
    connection = sql.connect('../database.db')
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sql.Row
    return connection
def get_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
def get_products(connection):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT products.product_name, products.price, products.quantity,categories.category_name
    FROM products
    JOIN categories
    ON categories.category_id = products.category_id""")
    return cursor.fetchall()
def get_user_by_id(connection,user_id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT username, email, city
    FROM users
    WHERE user_id = ?""",(user_id,))
    return cursor.fetchone()
def create_user(connection,username,email,city,registration_date):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO users(username,email,city,registration_date)
    VALUES (?,?,?,?,?)""",(username,email,city,registration_date))
    connection.commit()
    return cursor.lastrowid
def update_user(connection,user_id,username,email,city):
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE users
    SET username = ?, email = ?, city = ?
    WHERE user_id = ?""",(username,email,city,user_id))
    connection.commit()
    return cursor.rowcount
def delete_user(connection,user_id):
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM users
    WHERE user_id = ?""",(user_id,))
    connection.commit()
    return cursor.rowcount
def get_product_by_id(connection,product_id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * 
    FROM products
    WHERE product_id = ?""",(product_id,))
    return cursor.fetchone()
def get_product_by_category(connection,category_id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * 
    FROM products
    WHERE category_id = ?""",(category_id,))
    return cursor.fetchall()
def update_product_price(connection,price,product_id):
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE products
    SET price = ?
    WHERE product_id = ?""",(price,product_id))
    connection.commit()
    return cursor.rowcount
def update_product_quantity(connection,quantity,product_id):
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE products
    SET quantity = ?
    WHERE product_id = ?""",(quantity,product_id))
    connection.commit()
    return cursor.rowcount
def get_category_id(connection,category_name):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT category_id
    FROM categories
    WHERE category_name = ?""", (category_name,))
    return cursor.fetchone()
def get_orders(connection):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM orders""")
    return cursor.fetchall()
def get_order_by_id(connection,order_id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT *
    FROM orders
    WHERE order_id = ?""",(order_id,))
    return cursor.fetchone()
def get_order_items(connection, order_id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT products.product_name, order_items.quantity, product.price
    FROM order_items
    JOIN products
         ON products.product_id = order_items.product_id
    WHERE order_items.order_id = ?""",(order_id,))
    return cursor.fetchall()
def get_orders_by_user(connection,user_id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT *
    FROM orders
    WHERE user_id = ?""",(user_id,))
    return cursor.fetchall()