import analytics, database, pandas, sqlite3
def to_dataframe(rows):
    return pandas.DataFrame([dict(row) for row in rows])
def get_users():
    connection = database.get_connection()
    users = database.get_users(connection)
    connection.close()
    return to_dataframe(users)

def get_products():
    connection = database.get_connection()
    products = database.get_products(connection)
    connection.close()
    return to_dataframe(products)

def get_user_by_id(user_id):
    connection = database.get_connection()
    user = database.get_user_by_id(connection,user_id)
    connection.close()
    return user

def create_user(username,email,city,registration_date):
    connection = database.get_connection()
    try:
        user_id = database.create_user(connection,username,email,city,registration_date)
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()

def update_user(user_id,username,email,city):
    connection = database.get_connection()
    try:
        user = database.get_user_by_id(connection,user_id)
        if user is None:
            return None
        if not username:
            username = user['username']
        if not email:
            email = user['email']
        if not city:
            city = user['city']
        rowcount = database.update_user(connection,user_id,username,email,city)
        return rowcount
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()

def delete_user(user_id):
    connection = database.get_connection()
    try:
        rowcount = database.delete_user(connection,user_id)
        return rowcount
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()

def get_product_by_id(product_id):
    connection = database.get_connection()
    product = database.get_product_by_id(connection,product_id)
    connection.close()
    return product

def get_products_by_category(category_id):
    connection = database.get_connection()
    products = database.get_products_by_category(connection,category_id)
    connection.close()
    return to_dataframe(products)

def get_orders():
    connection = database.get_connection()
    orders = database.get_orders(connection)
    connection.close()
    return to_dataframe(orders)

def get_order_by_id(order_id):
    connection = database.get_connection()
    order = database.get_order_by_id(connection,order_id)
    connection.close()
    return order

def get_order_items(order_id):
    connection = database.get_connection()
    items = database.get_order_items(connection,order_id)
    connection.close()
    return to_dataframe(items)

def get_user_orders(user_id):
    connection = database.get_connection()
    orders = database.get_orders_by_user(connection,user_id)
    connection.close()
    return to_dataframe(orders)

def get_category_satistic():
    connection = database.get_connection()
    categories = database.get_category_statistic(connection)
    connection.close()
    return to_dataframe(categories)

def get_total_revenue():
    connection = database.get_connection()
    items = database.get_order_items_by_status(connection,"completed")
    items = to_dataframe(items)
    connection.close()
    return analytics.get_revenue(items)

def get_average_order_price():
    connection = database.get_connection()
    prices = database.get_orders_pricies(connection)
    prices = to_dataframe(prices)
    connection.close()
    return analytics.get_average_order_price(prices)

def get_orders_count():
    connection = database.get_connection()
    orders = database.get_orders(connection)
    orders = to_dataframe(orders)
    connection.close()
    return analytics.orders_count(orders)

def get_complete_orders_count():
    connection = database.get_connection()
    orders = database.get_orders(connection)
    orders = to_dataframe(orders)
    connection.close()
    return analytics.complete_orders_count(orders)

def get_most_sold_product():
    connection = database.get_connection()
    products = database.get_product_statistic(connection)
    products = to_dataframe(products)
    connection.close()
    return analytics.get_most_saled(products)

def get_most_profitable_product():
    connection = database.get_connection()
    products = database.get_product_statistic(connection)
    products = to_dataframe(products)
    connection.close()
    return analytics.get_most_profitable(products)

def get_least_sold_product():
    connection = database.get_connection()
    products = database.get_product_statistic(connection)
    products = to_dataframe(products)
    connection.close()
    return analytics.get_least_saled(products)

def get_most_purchases_user():
    connection = database.get_connection()
    users = database.get_users(connection)
    users = to_dataframe(users)
    connection.close()
    return analytics.get_most_purchases(users)

def get_least_purchases_user():
    connection = database.get_connection()
    users = database.get_users(connection)
    users = to_dataframe(users)
    connection.close()
    return analytics.get_least_purchases(users)

def get_most_sold_category():
    connection = database.get_connection()
    categories = database.get_category_statistic(connection)
    categories = to_dataframe(categories)
    connection.close()
    return analytics.get_most_saled_category(categories)

def get_category_name(category_id):
    connection=database.get_connection()
    category_name = database.get_category_name(connection,category_id)
    connection.close()
    if category_name is None:
        return None
    return category_name["category_name"]

def update_product(quantity,price,product_id):
    connection = database.get_connection()
    product = get_product_by_id(product_id)
    if product is None:
        connection.close()
        return None
    if quantity is None:
        quantity = product["quantity"]
    if price is None:
        price = product["price"]
    rowcount = database.update_product(connection,quantity,price,product_id)
    connection.close()
    return rowcount

def delete_order(order_id):
    connection = database.get_connection()
    try:
        rowcount = database.delete_order(connection,order_id)
        return rowcount
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()

def create_order(user_id,order_date,status):
    connection = database.get_connection()
    try:
        order_id = database.create_order(connection, user_id, order_date, status)
        return order_id
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()

def update_order(order_id,status):
    connection = database.get_connection()
    rowcount = database.update_order(connection,order_id, status)
    connection.close()
    return rowcount

def add_order_item(order_id,product_id,quantity,price_at_the_moment):
    connection = database.get_connection()
    try:
        order_item_id = database.add_order_item(connection, order_id, product_id, quantity, price_at_the_moment)
        return order_item_id
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()

def update_order_item(quantity,order_item_id):
    connection = database.get_connection()
    rowcount = database.update_order_item(connection, quantity, order_item_id)
    connection.close()
    return rowcount

def delete_order_item(order_item_id):
    connection = database.get_connection()
    rowcount = database.delete_order_item(connection, order_item_id)
    connection.close()
    return rowcount

def get_order_item_by_id(order_item_id):
    connection = database.get_connection()
    item = database.get_order_item_by_id(connection, order_item_id)
    connection.close()
    return item