
def orders_count(orders):
    return len(orders)


def complete_orders_count(orders):
    return len(orders[orders["status"]=="completed"])


def get_revenue(orders_items):
    return sum(orders_items['price_at_the_moment']*orders_items['quantity'])


def get_average_order_price(orders):
    if orders.empty:
        return 0
    return int(orders['order_total'].mean())


def get_most_saled(products):
    if products.empty:
        return ["-",0]
    sale_count = products["total_quantity"].max()
    product = products[products['total_quantity'] == sale_count]["product_name"].tolist()[0]
    result = [product, int(sale_count)]
    return result

def get_most_profitable(products):
    if products.empty:
        return ["-",0]
    revenue = products["revenue"].max()
    product = products[products["revenue"]==revenue]["product_name"].tolist()[0]
    result = [product,int(revenue)]
    return result


def get_least_saled(products):
    if products.empty:
        return ["-",0]
    sale_count = products['total_quantity'].min()
    product = products[products['total_quantity']==sale_count]["product_name"].tolist()[0]
    result=[product,int(sale_count)]
    return result

def get_most_purchases(users):
    if users.empty:
        return ["-", 0]
    sale_count = users["orders_count"].max()
    user = users[users['orders_count'] == sale_count]["username"].tolist()[0]
    result = [user, int(sale_count)]
    return result

def get_least_purchases(users):
    if users.empty:
        return ["-", 0]
    sale_count = users["orders_count"].min()
    user = users[users['orders_count'] == sale_count]["username"].tolist()[0]
    result = [user, int(sale_count)]
    return result

def get_most_saled_category(categories):
    if categories.empty:
        return ["-", 0]
    sale_count = categories["total_quantity"].max()
    category = categories[categories['total_quantity'] == sale_count]["category_name"].tolist()[0]
    result = [category, int(sale_count)]
    return result
