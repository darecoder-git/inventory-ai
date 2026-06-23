-- return customer rate


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




-- customer churn 


-- customer visit pattern



-- cohort analysis



-- customer product reviews 