CREATE OR REPLACE VIEW customer_cohort AS


WITH first_order AS (

SELECT
customer_id,
DATE_TRUNC(
'month',
MIN(order_date)
) cohort_month
FROM orders
GROUP BY 1

),

activity AS (
SELECT
o.customer_id,
DATE_TRUNC(
'month',
o.order_date
) active_month,
f.cohort_month
FROM orders o
JOIN first_order f
ON o.customer_id=f.customer_id
)

SELECT
cohort_month,
DATE_DIFF(
'month',
cohort_month,
active_month
) month_number,
COUNT(
DISTINCT customer_id
) active_users
FROM activity

GROUP BY 1,2;