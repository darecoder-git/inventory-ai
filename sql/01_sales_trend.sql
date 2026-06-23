-- mom revenue trends


CREATE OR REPLACE VIEW daily_sales AS

SELECT
CAST(order_date AS DATE) dt,
SUM(order_amount) revenue,
COUNT(*) orders,
COUNT(DISTINCT customer_id) customers
FROM orders
GROUP BY 1;

-- sales per month




-- future category wise sales forecast