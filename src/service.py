import analytics, database, pandas
def to_dataframe(rows):
    return pandas.DataFrame([dict(row) for row in rows])
def get_users():
    connection = database.get_connection()
    users = database.get_users(connection)
    return to_dataframe(users)

def get_products():
    connection = database.get_connection()
    products = database.get_products(connection)
    return to_dataframe(products)

def get_user_by_id(user_id):
    connection = database.get_connection()
    return database.get_user_by_id(connection,user_id)

def create_user(username,email,city,registration_date):
    connection = database.get_connection()
    id = database.create_user(connection,username,email,city,registration_date)
    return id

def update_user(user_id,username,email,city):
    connection = database.get_connection()
    id = database.update_user(connection,user_id,username,email,city)
    return id

def delete_user(user_id):
    connection = database.get_connection()
    id = database.delete_user(connection,user_id)
    return id

def get_product_by_id(product_id):
    connection = database.get_connection()
    return database.get_product_by_id(connection,product_id)

def get_products_by_category(category_id):
    connection = database.get_connection()
    products = database.get_products_by_category(connection,category_id)
    return to_dataframe(products)

def update_product_price(price,product_id):
    connection = database.get_connection()
    id = database.update_product_price(connection,price,product_id)
    return id

def update_product_quantity(quantity,product_id):
    connection = database.get_connection()
    id = database.update_product_quantity(connection,quantity,product_id)
    return id

def get_category_by_id(category_name):
    connection = database.get_connection()
    return database.get_category_id(connection,category_name)

def get_orders():
    connection = database.get_connection()
    orders = database.get_orders(connection)
    return to_dataframe(orders)

def get_order_by_id(order_id):
    connection = database.get_connection()
    return database.get_order_by_id(connection,order_id)

def get_order_items(order_id):
    connection = database.get_connection()
    items = database.get_order_items(connection,order_id)
    return to_dataframe(items)

def get_user_orders(user_id):
    connection = database.get_connection()
    orders = database.get_orders_by_user(connection,user_id)
    return to_dataframe(orders)
