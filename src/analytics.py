
def orders_count(orders):
    return len(orders)


def complete_orders_count(orders):
    return len(orders[orders["status"]=="completed"])


def get_revenue(orders_items):
    return sum(orders_items['price_at_the_moment']*orders_items['quantity'])


def get_average_order_price(orders):
    return orders['order_total'].mean()


def get_most_saled(products):
    sale_count = products["total_quantity"].max()
    result = products[products["total_quantity"]==sale_count]["product_name"].tolist()
    result.append(int(sale_count))
    return result

def get_most_profitable(products):
    revenue = products["revenue"].max()
    result = products[products["revenue"]==revenue]["product_name"].tolist()
    result.append(int(revenue))
    return result


def get_least_saled(products):
    return products[products["total_quantity"]==min(products["total_quantity"])]


def get_user_most_purchases(users):
    return users[users['orders_count']==max(users['orders_count'])]


def get_user_least_purchases(users):
    return users[users['orders_count'] == min(users['orders_count'])]