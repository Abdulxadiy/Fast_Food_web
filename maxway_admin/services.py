from django.db import connection
from contextlib import closing


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_order_by_user(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT maxway_users_order.id, maxway_users_users.first_name,maxway_users_users.last_name, maxway_users_order.address, maxway_users_order.payment_type,maxway_users_order.status,maxway_users_order.created_at from maxway_users_order 
                            INNER JOIN maxway_users_users on maxway_users_users.id=maxway_users_order.customer_id 
                            where maxway_users_order.customer_id =%s""", [id])
        order = dictfetchall(cursor)
        return order


def get_product_by_order(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT maxway_users_orderproduct.count,maxway_users_orderproduct.price,
        maxway_users_orderproduct.created_at,maxway_users_product.name from maxway_users_orderproduct 
         INNER JOIN maxway_users_product ON maxway_users_orderproduct.product_id=maxway_users_product.id  where order_id=%s""", [id])
        order_product = dictfetchall(cursor)
        return order_product


def get_table():
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" 
        SELECT maxway_users_orderproduct.product_id, 
COUNT(maxway_users_orderproduct.product_id),maxway_users_product.name 
FROM maxway_users_orderproduct 
INNER JOIN maxway_users_product ON maxway_users_product.id=maxway_users_orderproduct.product_id 
GROUP BY maxway_users_orderproduct.product_id ,maxway_users_product.name 
order by count desc limit 10

        """)
        table = dictfetchall(cursor)
        return table
