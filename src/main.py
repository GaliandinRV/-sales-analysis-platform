from fastapi import FastAPI
import service
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
    </form>"""

@app.get('/orders/by_user_id',response_class=HTMLResponse)
def get_user_orders(user_id: int):
