-- bestselling products

CREATE OR REPLACE VIEW product_performance AS

SELECT
p.product_name,

SUM(oi.quantity) units_sold,

SUM(
oi.quantity * oi.price
) revenue

FROM order_items oi

JOIN products p
ON oi.product_id = p.product_id

GROUP BY 1;

-- not so best selling




-- product ratings and reviews 
