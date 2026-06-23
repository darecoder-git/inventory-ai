-- sale velocity

import numpy as np
import pandas as pd

products = con.sql("""
SELECT DISTINCT product_id
FROM products
""").df()

products["stock_qty"] = np.random.randint(
5,
500,
len(products)
)

con.register("inventory_df", products)

-- con.execute("""
-- CREATE TABLE inventory AS
-- SELECT *
-- FROM inventory_df
-- """)



-- inventory / velocity for product (understock , overstock)

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





