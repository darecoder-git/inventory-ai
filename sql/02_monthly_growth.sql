CREATE OR REPLACE VIEW monthly_growth AS

WITH monthly AS (

SELECT
DATE_TRUNC('month', order_date) month,
SUM(order_amount) revenue
FROM orders
GROUP BY 1

)

SELECT
month,
revenue,

LAG(revenue) OVER(
ORDER BY month
) prev_revenue,

ROUND(
100.0 *
(revenue - LAG(revenue) OVER(ORDER BY month))
/
NULLIF(LAG(revenue) OVER(ORDER BY month),0),
2
) mom_growth

FROM monthly;