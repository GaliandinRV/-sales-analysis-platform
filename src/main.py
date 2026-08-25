from fastapi import FastAPI, Form
import service
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
    <a href="/categories">Categories</a><br>"""

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
    <form action="/orders/by_user_id" method="get">
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
    html = f"""
    <a href="/">menu</a><br>
    <h1>Order ID {order_id} items:</h1>
    <table border="1">
        <tr>
            <th>product name</th>
            <th>quantity</th>
            <th>price at the moment</th>
        </tr>"""
    for ind,item in items.iterrows():
        html+=f"""
        <tr>
            <td>{item['product_name']}</td>
            <td>{item['quantity']}</td>
            <td>{item['price_at_the_moment']}</td>
        </tr>"""
    html+="""
    </table>"""
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
    return f"""
    <h1>User created!<h1>
    <p>User ID:{user_id}</p>
    <a href="/users">Back to users</a><br>"""

@app.get('/users/update/{user_id}',response_class=HTMLResponse)
def update_user_form(user_id: int):
    return f"""
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
    return f"""
    <h1>User with id {user_id} update</h1>"""

@app.get('/orders',response_class=HTMLResponse)
def get_orders():
    html = f"""
    <h1>Orders</h1>
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
            <td>{order["order_id"]}</td>
            <td>{order["user_id"]}</td>
            <td>{order["order_date"]}</td>
            <td>{order["status"]}</td>
        </tr>"""
    html+="""
    </table"""
    return html

@app.get('/products',response_class=HTMLResponse)
def get_products():
    html = f"""
        <h1>Products</h1>
        <table border="1">
            <tr>
                <th>Product ID</th>
                <th>Product name</th>
                <th>Category ID</th>
                <th>price</th>
                <th>quantity</th>
            </tr>
        """
    products = service.get_products()
    for ind, product in products.iterrows():
        html += f"""
            <tr>
                <td>{product["product_id"]}</td>
                <td>{product["product_name"]}</td>
                <td>{product["category_name"]}</td>
                <td>{product["price"]}</td>
                <td>{product["quantity"]}</td>
            </tr>"""
    html += """
        </table"""
    return html

@app.get('/categories',response_class=HTMLResponse)
def get_categories():
    html = f"""
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
                <td>{category["category_id"]}</td>
                <td>{category["category_name"]}</td>
                <td>{category["total_quantity"]}</td>
                <td>{category["revenue"]}</td>
            </tr>"""
    html += """
        </table"""
    return html

