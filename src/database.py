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
def det_user_by_id(connection,id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT username, email, city
    FROM users
    WHERE user_id = ?""",(id,))
    return cursor.fetchone()
