import database as db
import analytics
connection = db.get_connection()
# print(analytics.complete_orders_count(analytics.to_dataframe(db.get_orders(connection))))
products = db.get_product_statistic(connection)
for n in products:
    for s in n:
        print(s)
print(analytics.get_most_saled(analytics.to_dataframe(products)))
print(analytics.get_most_profitable(analytics.to_dataframe(products)))
print(analytics.get_least_saled(analytics.to_dataframe(products)))
categories = analytics.to_dataframe(db.get_category_statistic(connection))
print(analytics.get_most_saled(categories))
print('###')
users = db.get_user_statistic(connection)

for i in users:
    print([n for n in i])