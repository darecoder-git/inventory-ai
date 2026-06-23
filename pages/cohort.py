cohort=conn.sql(
"""
SELECT *
FROM customer_cohort
""").df()
pivot=cohort.pivot(
index="cohort_month",
columns="month_number",
values="active_users"
)

px.imshow(pivot)