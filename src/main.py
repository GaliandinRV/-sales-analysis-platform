from fastapi import FastAPI, Form
from src import service
from datetime import date
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get('/',response_class=HTMLResponse)
def home():
    return """
    <h1>sales analysis platform</h1>
    
    <a href="/users">Users</a><br>
    <a href="/orders">Orders</a><br>
    <a href="/products">Products</a><br>
    <a href="/categories">Categories</a><br>
    <a href="/analitics">Analitics</a><br>"""

@app.get("/users",response_class=HTMLResponse)
def get_users():
    users = service.get_users()
    html =  """
    <h1>Users</h1>
    
    <a href="/">menu</a><br>
    <a href="/users/add">Add user</a><br>
    <form action="/users/id" method="get">
        <input type="number" name="user_id" placeholder="User ID">
        <button type="submit">Show user</button>
    </form>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Orders count</th>
        </tr>
    """
    for ind, user in users.iterrows():
        html+=f"""
        <tr>
            <td>{user['user_id']}</td>
            <td>{user['username']}</td>
            <td>{user['orders_count']}</td>
        </tr>"""
    html+="</table>"
    return html

@app.get('/users/id',response_class=HTMLResponse)
def get_user_by_id(user_id: int):
    user = service.get_user_by_id(user_id)
    if user is None:
        return """
        <a href="/">menu</a><br>
        <h1>User not found!<h1>"""
    return f"""
    <a href="/">menu</a><br>
    
    <h1>User with ID = {user_id}</h1>

    <h2>username: {user['username']}</h2>
    <h2>email: {user['email']}</h2>
    <h2>city: {user['city']}</h2>
    <h2>orders count:{user['orders_count']}</h2>
    <h2>total quantity:{user['total_quantity']}</h2>
    <h2>revenue:{user['revenue']}</h2>

    <form action="/orders/by_user_id" method="get">
        <input type="hidden" name="user_id" value="{user_id}">
        <button type="submit">User orders</button>
    </form>
    <form action="/users/update/{user_id}" method="get">
        <button type="submit">Update user</button>
    </form>
    <form action="/users/delete" method="post">
        <input type="hidden" name="user_id" value="{user_id}">
        <button type="submit">Delete user</button>
    </form>"""

@app.get('/orders/by_user_id',response_class=HTMLResponse)
def get_user_orders(user_id: int):
    orders = service.get_user_orders(user_id)
    html = f"""
    <a href="/">menu</a><br>
    <h1>User ID {user_id} orders:</h1>
    <table border="1">
        <tr>
            <th>order ID</th>
            <th>date</th>
            <th>status</th>
        </tr>"""
    for ind,order in orders.iterrows():
        html+=f"""
        <tr>
            <td><a href="/orders/items/{order['order_id']}">{order['order_id']}</a><br></td>
            <td>{order['order_date']}</td>
            <td>{order['status']}</td>
        </tr>"""
    html+="""
    </table>"""
    return html

@app.get('/orders/items/{order_id}',response_class=HTMLResponse)
def get_order_items(order_id: int):
    items = service.get_order_items(order_id)
    total_price=0
    order = service.get_order_by_id(order_id)
    if order is None:
        return """
        <Order not found!"""
    html = f"""
    <a href="/">menu</a><br>
    <h1>Order ID {order_id} items:</h1>
    <h3>Status: {order["status"]}</h3>
    <form action="/orders/update" method="post">
        <input type="hidden" name="order_id" value="{order_id}">
        <select name="status">
            <option value="completed">completed</option>
            <option value="shipped">shipped</option>
            <option value="cancelled">cancelled</option>
            <option value="processing">processing</option>
        </select>
        <button type="submit">Update</button>
    </form>
    <h3>Add item:</h3>
    <form action='/items/add' method='post'>
        <select name="product_id">"""
    products = service.get_products()
    for ind, product in products.iterrows():
        html+=f"""
            <option value="{product['product_id']}">{product['product_name']}</option>"""
    html+=f"""
        </select>
        <input type="number" name="quantity" placeholder="Quantity:">
        <input type="hidden" name="order_id" value="{order_id}">
        <button type="submit">Create</button>
    </form>
    <form action="/orders/delete" method="post">
        <input type="hidden" name="order_id" value="{order_id}">
        <button type="submit">Delete order</button>
    </form>
    <table border="1">
        <tr>
            <th>product name</th>
            <th>quantity</th>
            <th>price at the moment</th>
        </tr>"""
    for ind,item in items.iterrows():
        total_price+=item['price_at_the_moment']*item['quantity']
        html+=f"""
        <tr>
            <td><a href="/items/{item["order_item_id"]}">{item['product_name']}</a><br></td>
            <td>{item['quantity']}</td>
            <td>{item['price_at_the_moment']}</td>
        </tr>"""
    html+=f"""
    </table>
    <h1>Total price: {total_price}</h1>"""
    return html

@app.get('/users/add',response_class=HTMLResponse)
def add_user_form():
    return """
    <a href="/">menu</a><br>
    
    <h1>Create user</h1>
    
    <form action="/users/add" method="post">
        <input type="text" name="username" placeholder="Username">
        <input type="email" name="email" placeholder="Email">
        <input type="text" name="city" placeholder="City">
        <button type="submit">Create</button>
    </form>"""

@app.post('/users/add',response_class=HTMLResponse)
def create_user(
        username: str = Form(),
        email: str = Form(),
        city:str = Form()
):
    registration_date = date.today()
    user_id = service.create_user(username,email,city,registration_date)
    if user_id is None:
        return """
        <a href="/users">Back to users</a><br>
        <h1>User not created!</h1>"""
    return f"""
    <h1>User created!<h1>
    <p>User ID:{user_id}</p>
    <a href="/users">Back to users</a><br>"""

@app.get('/users/update/{user_id}',response_class=HTMLResponse)
def update_user_form(user_id: int):
    return f"""
    <a href="/">menu</a><br>
    <form action="/users/update/{user_id}" method="post">
        <input type="text" name="username" placeholder="Username:">
        <input type="email" name="email" placeholder="Email:">
        <input type="text" name="city" placeholder="City:">
        <button type="submit">Update</button>
    </form>"""

@app.post('/users/update/{user_id}',response_class=HTMLResponse)
def update_user(
        user_id: int,
        username: str = Form(""),
        email : str = Form(""),
        city: str = Form("")
):
    result = service.update_user(user_id,username,email,city)
    if result is None:
        return """
                <a href="/users">Back to users</a><br>
                <h1>User not updated!</h1>"""
    return f"""
    <a href="/">menu</a><br>
    <h1>User with id {user_id} update</h1>"""

@app.get('/orders',response_class=HTMLResponse)
def get_orders():
    html = f"""
    <a href="/">menu</a><br>
    <h1>Orders</h1>
    <a href='/orders/create'>Create order</a><br>
    <table border="1">
        <tr>
            <th>Order ID</th>
            <th>User ID</th>
            <th>Order date</th>
            <th>Status</th>
        </tr>
    """
    orders = service.get_orders()
    for ind, order in orders.iterrows():
        html+=f"""
        <tr>
            <td><a href="/orders/items/{order["order_id"]}">{order["order_id"]}</a><br></td>
            <td>{order["user_id"]}</td>
            <td>{order["order_date"]}</td>
            <td>{order["status"]}</td>
        </tr>"""
    html+="""
    </table>"""
    return html

@app.get('/products',response_class=HTMLResponse)
def get_products():
    html = f"""
        <a href="/">menu</a><br>
        <h1>Products</h1>
        <table border="1">
            <tr>
                <th>Product ID</th>
                <th>Product name</th>
                <th>Category</th>
                <th>price</th>
                <th>quantity</th>
            </tr>
        """
    products = service.get_products()
    for ind, product in products.iterrows():
        html += f"""
            <tr>
                <td><a href="/products/{product["product_id"]}">{product["product_id"]}</a><br></td>
                <td>{product["product_name"]}</td>
                <td>{product["category_name"]}</td>
                <td>{product["price"]}</td>
                <td>{product["quantity"]}</td>
            </tr>"""
    html += """
        </table>"""
    return html

@app.get('/categories',response_class=HTMLResponse)
def get_categories():
    html = f"""
        <a href="/">menu</a><br>
        <h1>Categories</h1>
        <table border="1">
            <tr>
                <th>Category ID</th>
                <th>Category name</th>
                <th>Category quantity</th>
                <th>Category revenue</th>
            </tr>
        """
    categories = service.get_category_satistic()
    for ind, category in categories.iterrows():
        html += f"""
            <tr>
                <td><a href="/categories/{category["category_id"]}">{category["category_id"]}</a><br></td>
                <td>{category["category_name"]}</td>
                <td>{category["total_quantity"]}</td>
                <td>{category["revenue"]}</td>
            </tr>"""
    html += """
        </table>"""
    return html

@app.get('/analitics',response_class=HTMLResponse)
def get_analitics():
    total_revenue = service.get_total_revenue()
    average = service.get_average_order_price()
    orders_count = service.get_orders_count()
    complete_orders_count = service.get_complete_orders_count()
    most_sold_product = service.get_most_sold_product()
    least_sold_product = service.get_least_sold_product()
    most_profitable_product = service.get_most_profitable_product()
    most_purchase_user = service.get_most_purchases_user()
    least_purchase_user = service.get_least_purchases_user()
    most_sold_category = service.get_most_sold_category()
    return f"""
    <a href="/">menu</a><br>
    <h1>Analitics</h1>
    <h2>Orders</h2>
    <p>Total revenue: {total_revenue}</p>
    <p>Average order: {average}</p>
    <p>Orders: {orders_count}</p>
    <p>Complete orders: {complete_orders_count}</p>
    <h2>Products</h2>
    <p>Most sold: {most_sold_product[0]} {most_sold_product[1]}</p>
    <p>Least sold: {least_sold_product[0]} {least_sold_product[1]}</p>
    <p>Most profitable: {most_profitable_product[0]} {most_profitable_product[1]}</p>
    <h2>Users</h2>
    <p>Most purchases: {most_purchase_user[0]} {most_purchase_user[1]}</p>
    <p>Least purchases: {least_purchase_user[0]} {least_purchase_user[1]}</p>
    <h2>Category</h2>
    <p>Best category: {most_sold_category[0]} {most_sold_category[1]}</p>"""

@app.post("/users/delete",response_class=HTMLResponse)
def delete_user(user_id: int = Form()):
    rows = service.delete_user(user_id)
    if rows is None:
        return """
        <a href="/">menu</a><br>
        <h1>User cant be deleted!</h1>
        """
    elif rows > 0:
        return f"""
        <a href="/">menu</a><br>
        <h1>User with id:{user_id} has been delete</h1>"""
    else:
        return f"""
        <a href="/">menu</a><br>
        <h1>User with id:{user_id} dont exist</h1>"""

@app.get('/categories/{category_id}',response_class=HTMLResponse)
def get_products_by_category_id(category_id: int):
    products = service.get_products_by_category(category_id)
    category_name = service.get_category_name(category_id)
    if category_name is None:
        return """
        <a href="/">menu</a><br>
        <h1>Category not found!</h1>
        """
    html = f"""
    <a href="/">menu</a><br>
    <h1>{category_name} products:</h1>
    <table border="1">
        <tr>
            <th>Product ID</th>
            <th>Product name</th>
            <th>Price</th>
            <th>Quantity</th>
        </tr>"""
    for ind,product in products.iterrows():
        html += f"""
        <tr>
            <td>{product["product_id"]}</td>
            <td>{product["product_name"]}</td>
            <td>{product["price"]}</td>
            <td>{product["quantity"]}</td>
        </tr>"""
    html+="""
    </table>"""
    return html

@app.get("/products/update",response_class=HTMLResponse)
def update_product_form(product_id: int):
    return f"""
<a href="/">menu</a><br>
<form action="/products/update" method="post">
    <input type="number" name="new_price" placeholder="new price:">
    <input type="number" name="new_quantity" placeholder="new quantity:">
    <input type="hidden" name="product_id" value="{product_id}">
    <button type="submit">Update</button>
</form>"""

@app.post("/products/update",response_class=HTMLResponse)
def update_product(
        product_id: int = Form(),
        new_price: int | None = Form(None),
        new_quantity: int | None = Form(None)
):
    if (new_quantity is not None and new_quantity<1) or (new_price is not None and new_price<1):
        return """
        <a href="/">menu</a><br>
        <h1>Product hasnt been update</h1>"""
    result = service.update_product(new_quantity, new_price, product_id)
    if result is None:
        return """
        <a href="/">menu</a><br>
        <h1>Product not found!</h1>
        """
    return """
    <a href="/">menu</a><br>
    <h1>Product has been update</h1>"""

@app.get("/products/{product_id}",response_class=HTMLResponse)
def get_product_by_id(product_id: int):
    product = service.get_product_by_id(product_id)
    if product is None:
        return """
        <a href="/">menu</a><br>
        <h1>Product not found!</h1>
        """
    category_name = service.get_category_name(product["category_id"])
    if category_name is None:
        return """
        <a href="/">menu</a><br>
        <h1>Category not found!</h1>
        """
    return f"""
    <a href="/">menu</a><br>
    <h1>Product ID: {product_id}</h1>
    <h1>Product name: {product["product_name"]}</h1>
    <h1>Product category: {category_name}</h1>
    <h1>Product price: {product["price"]}</h1>
    <h1>Product quantity: {product["quantity"]}</h1>
    <form action="/products/update" method="get">
        <input type="hidden" name="product_id" value="{product_id}">
        <button type="submit">Update product</button>
    </form>"""

@app.get('/items/{order_item_id}',response_class=HTMLResponse)
def get_items(order_item_id: int):
    item = service.get_order_item_by_id(order_item_id)
    if item is None:
        return """
        <a href="/">menu</a><br>
        <h1>Item not found!</h1>
        """
    product = service.get_product_by_id(item['product_id'])
    if product is None:
        return """
        <a href="/">menu</a><br>
        <h1>Product not found!</h1>
        """
    return f"""
<a href="/">menu</a><br>
<h1>Order item ID {order_item_id}</h1>
<h2>Product name: {product['product_name']}</h2>
<h2>Order ID: {item['order_id']}</h2>
<h2>Quantity: {item['quantity']}</h2>
<h2>Price at the moment: {item['price_at_the_moment']}</h2>
<h3>Edit quantity:</h3>
<form action="/items/update/{order_item_id}" method="post">
    <input type="number" name="quantity" placeholder="quantity:">
    <button type="submit">Update</button>
</form>
<form action="/items/delete" method="post">
    <input type="hidden" name="order_item_id" value="{order_item_id}">
    <button type="submit">Delete</button>
</form>
<h3></h3>"""

@app.post('/items/update/{order_item_id}',response_class=HTMLResponse)
def update_item(order_item_id: int,quantity:int = Form()):
    if quantity<1:
        return """
        <a href="/">menu</a><br>
        <h1>item quantity dasnt updated!"""
    result = service.update_order_item(quantity, order_item_id)
    if result == 0:
        return """<a href="/">menu</a><br>
        <h1>Item not found!</h1>
        """
    return """
    <a href="/">menu</a><br>
    <h1>Item quantity updated!</h1>"""

@app.post('/items/delete',response_class=HTMLResponse)
def delete_item(order_item_id: int = Form()):
    result = service.delete_order_item(order_item_id)
    if result == 0:
        return """<a href="/">menu</a><br>
        <h1>Item not found!</h1>
        """
    return """
    <a href="/">menu</a><br>
    <h1>Item deleted!</h1>"""

@app.post('/items/add',response_class=HTMLResponse)
def add_item(product_id: int = Form(),order_id: int = Form(),quantity: int = Form()):
    if quantity<1:
        return """
        <a href="/">menu</a><br>
        <h1>Item dont added!</h1>"""
    product = service.get_product_by_id(product_id)
    if product is None:
        return """
        <a href="/">menu</a><br>
        <h1>Product not exist!</h1>"""
    price = product['price']
    order_item_id = service.add_order_item(order_id,product_id,quantity,price)
    if order_item_id is None:
        return """
        <a href="/">menu</a><br>
        <h1>Item dont added!</h1>"""
    return """
    <a href="/">menu</a><br>
    <h1>Item added!</h1>"""

@app.post('/orders/delete',response_class=HTMLResponse)
def delete_order(order_id: int = Form()):
    rowcount = service.delete_order(order_id)
    if rowcount is None:
        return """
    <a href="/users">Back to users</a><br>
    <h1>Order dont deleted!</h1>"""
    if rowcount == 0:
        return """
    <a href="/">menu</a><br>
    <h1>Order not deleted</h1>"""
    return """
    <a href="/">menu</a><br>
    <h1>Order deleted</h1>"""

@app.get('/orders/create',response_class=HTMLResponse)
def create_order_form():
    return """
    <a href="/">menu</a><br>
    <h1>Create order</h1>
    <form action="/orders/create" method="post">
        <input type="number" name="user_id" placeholder="user ID">
        <select name="status">
            <option value="completed">completed</option>
            <option value="shipped">shipped</option>
            <option value="cancelled">cancelled</option>
            <option value="processing">processing</option>
        </select>
        <button type="submit">Create</button>
    </form>"""

@app.post('/orders/create',response_class=HTMLResponse)
def create_order(user_id: int = Form(), status: str = Form()):
    user = service.get_user_by_id(user_id)
    if user is None:
        return """
        <a href="/">menu</a><br>
        <h1>User not exist</h1>"""
    order_date = date.today()
    order_id = service.create_order(user_id, order_date, status)
    if order_id is None:
        return """
        <a href="/users">Back to users</a><br>
        <h1>Order not created</h1>"""
    return """
    <a href="/">menu</a><br>
    <h1>Order created</h1>"""

@app.post('/orders/update',response_class=HTMLResponse)
def update_order(order_id: int = Form(), status: str = Form()):
    result = service.update_order(order_id, status)
    if result == 0:
        return """
        <a href="/">menu</a><br>
        <h1>Order not found!</h1>
        """
    return """
    <a href="/">menu</a><br>
    <h1>Order status updated!</h1>"""