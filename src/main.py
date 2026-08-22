import database as db
connection = db.get_connection()
products = db.get_products(connection)
# for i in products:
#     print(i['product_name'],i['category_name'])
user = db.det_user_by_id(db.get_connection(),1)
print(user['username'],user['email'])