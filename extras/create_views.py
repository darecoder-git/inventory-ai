import duckdb 
import pandas as pd
import numpy as np
conn=duckdb.connect('./merchant_db.db')
print(conn.table.__name__)


# daily revenue view
# conn.execute(
# """
# CREATE OR REPLACE VIEW daily_revenue
# AS (
# select 
# CAST(o.order_date as date) AS order_date,
# count(o.order_id) as total_orders,
# count(distinct i.product_id) as products_sold,
# count(distinct o.user_id) as customers_number,
# round(sum(o.total_amount),2) as revenue
# from orders o
# join order_items i on o.order_id=i.order_id
# group by 1 )
# """
# )

# conn.sql("""
# select 
# CAST(o.order_date as date) AS order_date,
# count(o.order_id) as total_orders,
# count(distinct i.product_id) as products_sold,
# count(distinct o.user_id) as customers_number,
# round(sum(o.total_amount),2) as revenue
# from orders o
# join order_items i on o.order_id=i.order_id
# group by 1 
# """).show()





# conn.execute(
# """
# CREATE OR REPLACE VIEW monthly_growth AS

# WITH monthly AS (
#     SELECT
#         DATE_TRUNC('month', order_date) as month,
#         ROUND(SUM(total_amount),2) as revenue
#     FROM orders
#     GROUP BY 1
# )

# SELECT
#     month,
#     revenue,
#     LAG(revenue) OVER(ORDER BY month) as prev_revenue,
#     ROUND(
#         100.0 *
#         (revenue - LAG(revenue) OVER(ORDER BY month))
#         /
#         NULLIF(LAG(revenue) OVER(ORDER BY month),0),
#         2
#     ) mom_growth
# FROM monthly
# """)



# conn.sql(
# """
# --CREATE OR REPLACE VIEW product_performance AS
# SELECT
#     p.product_name,
#     SUM(oi.quantity) units_sold,
#     ROUND(SUM(oi.quantity * oi.item_price),2) revenue
# FROM order_items oi
# JOIN products p
# ON oi.product_id = p.product_id
# GROUP BY 1;
# """).show()





# conn.execute(
# """
# CREATE OR REPLACE VIEW product_performance AS
# SELECT
#     p.product_name,
#     SUM(oi.quantity) units_sold,
#     ROUND(SUM(oi.quantity * oi.item_price),2) revenue
# FROM order_items oi
# JOIN products p
# ON oi.product_id = p.product_id
# GROUP BY 1;
# """)


# # create an estimated inventory as dataset
# products = conn.sql("""
# SELECT DISTINCT product_id
# FROM products
# """).df()

# products["stock_qty"] = np.random.randint(
#     5,
#     150,
#     len(products)
# )

# conn.register("inventory_df", products)

# conn.execute("""
# CREATE OR REPLACE TABLE inventory AS
# SELECT *
# FROM inventory_df
# """)

conn.sql(
"""
SELECT *
FROM inventory
""").show()






conn.execute(
"""
CREATE OR REPLACE VIEW inventory_health AS
WITH sales AS
(SELECT
    i.product_id,
    MIN(o.order_date) first_sale,
    MAX(o.order_date) last_sale,
    SUM(i.quantity) units_sold
FROM order_items i
join orders o on i.order_id=o.order_id
GROUP BY i.product_id
),

velocity as(
SELECT
    product_id,
    units_sold /
    NULLIF(
        DATEDIFF('day', first_sale, last_sale) + 1,
        0
    ) AS avg_daily_velocity
FROM sales
)

select 
i.product_id,
(i.stock_qty / v.avg_daily_velocity) as days_remaining
from inventory i
join velocity v on i.product_id=v.product_id
""")






conn.execute(
"""
CREATE OR REPLACE VIEW customer_metrics AS
WITH customer_orders AS (
SELECT
    user_id,
    COUNT(*) order_count
FROM orders
GROUP BY 1
)

--add a date parameter to have clarity on orders on different dates
SELECT
    COUNT(*) total_customers,

    SUM(
        CASE
            WHEN order_count = 1
            THEN 1
            ELSE 0
        END
    ) single_order_customers,
    SUM(
        CASE
            WHEN order_count = 2
            THEN 1
            ELSE 0
        END
    ) returning_customers_2_orders,
     SUM(
        CASE
            WHEN order_count > 2
            THEN 1
            ELSE 0
        END
    ) returning_customers_3_orders_or_more

FROM customer_orders;
"""
)



conn.close()