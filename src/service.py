import analytics, database, pandas, sqlite3
def to_dataframe(rows):
    return pandas.DataFrame([dict(row) for row in rows])
def with_connection(function):
    connection = database.get_connection()
    try:
        return function(connection)
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()

def get_users():
    return with_connection(lambda connection: to_dataframe(database.get_users(connection)))

def get_products():
    return with_connection(lambda connection: to_dataframe(database.get_products(connection)))

def get_user_by_id(user_id):
    return with_connection(lambda connection: database.get_user_by_id(connection,user_id))

def create_user(username,email,city,registration_date):
    return with_connection(lambda connection: database.create_user(connection,username,email,city,registration_date))

def update_user(user_id, username, email, city):
    def update(connection):
        user = database.get_user_by_id(connection, user_id)
        if user is None:
            return None
        if not username:
            username = user['username']
        if not email:
            email = user['email']
        if not city:
            city = user['city']
        return database.update_user(connection,user_id,username,email,city)
    return with_connection(update)

def delete_user(user_id):
    return with_connection(lambda connection: database.delete_user(connection,user_id))
def get_product_by_id(product_id):
    return with_connection(lambda connection: database.get_product_by_id(connection,product_id))

def get_products_by_category(category_id):
    return with_connection(lambda connection: to_dataframe(database.get_products_by_category(connection,category_id)))

def get_orders():
    return with_connection(lambda connection: to_dataframe(database.get_orders(connection)))

def get_order_by_id(order_id):
    return with_connection(lambda connection: database.get_order_by_id(connection,order_id))

def get_order_items(order_id):
    return with_connection(lambda connection: to_dataframe(database.get_order_items(connection,order_id)))

def get_user_orders(user_id):
    return with_connection(lambda connection: to_dataframe(database.get_orders_by_user(connection,user_id)))

def get_category_satistic():
    return with_connection(lambda connection: to_dataframe(database.get_category_statistic(connection)))

def get_total_revenue():
    return analytics.get_revenue(with_connection(lambda connection: to_dataframe(database.get_order_items_by_status(connection,"completed"))))

def get_average_order_price():
    return analytics.get_average_order_price(with_connection(lambda connection: to_dataframe(database.get_orders_pricies(connection))))

def get_orders_count():
    return analytics.orders_count(with_connection(lambda connection: to_dataframe(database.get_orders(connection))))

def get_complete_orders_count():
    return analytics.complete_orders_count(with_connection(lambda connection: to_dataframe(database.get_orders(connection))))

def get_most_sold_product():
    return analytics.get_most_saled(with_connection(lambda connection: to_dataframe(database.get_product_statistic(connection))))

def get_most_profitable_product():
    return analytics.get_most_profitable(with_connection(lambda connection: to_dataframe(database.get_product_statistic(connection))))

def get_least_sold_product():
    return analytics.get_least_saled(with_connection(lambda connection: to_dataframe(database.get_product_statistic(connection))))

def get_most_purchases_user():
    return analytics.get_most_purchases(with_connection(lambda connection: to_dataframe(database.get_users(connection))))

def get_least_purchases_user():
    return analytics.get_least_purchases(with_connection(lambda connection: to_dataframe(database.get_users(connection))))

def get_most_sold_category():
    return analytics.get_most_saled_category(with_connection(lambda connection: to_dataframe(database.get_category_statistic(connection))))

def get_category_name(category_id):
    def get_name(connection):
        category_name = database.get_category_name(connection,category_id)
        if category_name is None:
            return None
        return category_name['category_name']
    return with_connection(get_name)

def update_product(quantity,price,product_id):
    def update(connection):
        product = database.get_product_by_id(connection, product_id)
        if product is None:
            return None
        if quantity is None:
            quantity = product["quantity"]
        if price is None:
            price = product["price"]
        return database.update_product(connection,quantity,price,product_id)
    return with_connection(update)

def delete_order(order_id):
    return with_connection(lambda connection: database.delete_order(connection,order_id))

def create_order(user_id,order_date,status):
    return with_connection(lambda connection: database.create_order(connection,user_id,order_date,status))

def update_order(order_id,status):
    return with_connection(lambda connection: database.update_order(connection,order_id,status))

def add_order_item(order_id,product_id,quantity,price_at_the_moment):
    return with_connection(lambda connection: database.add_order_item(connection,order_id,product_id,quantity,price_at_the_moment))

def update_order_item(quantity,order_item_id):
    return with_connection(lambda connection: database.update_order_item(connection,quantity,order_item_id))

def delete_order_item(order_item_id):
    return with_connection(lambda connection: database.delete_order_item(connection,order_item_id))

def get_order_item_by_id(order_item_id):
    return with_connection(lambda connection: database.get_order_item_by_id(connection,order_item_id))