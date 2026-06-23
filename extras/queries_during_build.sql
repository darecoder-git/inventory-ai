

# DATA_PROJECTS/merchant_insights/data/ecommerce_dataset/orders.csv
# orders
# conn.execute(
#     "CREATE OR REPLACE TABLE orders as select * from  '/Users/purkayastha7/Desktop/Codes/DATA_PROJECTS/merchant_insights/data/ecommerce_dataset/orders.csv' "
# )
# users
# conn.execute(
#     "CREATE OR REPLACE TABLE users as select * from  '/Users/purkayastha7/Desktop/Codes/DATA_PROJECTS/merchant_insights/data/ecommerce_dataset/users.csv'"
# )

# print("created")
# # profcud
# conn.execute(
#     "CREATE OR REPLACE TABLE products as select * from  '/Users/purkayastha7/Desktop/Codes/DATA_PROJECTS/merchant_insights/data/ecommerce_dataset/products.csv'"
# )
# # events
# conn.execute(
#     "CREATE OR REPLACE TABLE events as select * from  '/Users/purkayastha7/Desktop/Codes/DATA_PROJECTS/merchant_insights/data/ecommerce_dataset/events.csv'"
# )
# # reviews
# conn.execute(
#     "CREATE OR REPLACE TABLE reviews as select * from  '/Users/purkayastha7/Desktop/Codes/DATA_PROJECTS/merchant_insights/data/ecommerce_dataset/reviews.csv'"
# )
# # order_items
# conn.execute(
#     "CREATE OR REPLACE TABLE order_items as select * from  '/Users/purkayastha7/Desktop/Codes/DATA_PROJECTS/merchant_insights/data/ecommerce_dataset/order_items.csv'"
# )


# conn.sql("select * from orders where year(order_date)=2025 and total_amount>=2000").show()

# Let’s say you work at Shopify. Your team is building a dashboard for merchants that provides personalized 
# insights on sales trends, 
# inventory status (e.g., overstocked or low-stock items), 
# and customer behavior (e.g., new vs. returning customers) 
# based on transaction history and seasonal trends. 
# The goal is to help shop owners make better day-to-day decisions through clear and actionable data. What key metrics and visualizations would you include in the dashboard, and how would you ensure they remain useful across different types of merchants?"













# insights on sales trends, 
# mom sales trend

# conn.sql(
# """
# with cte as (
# select 
# datetrunc('month',order_date) as month,
# sum(total_amount) as current_month_total,
# from orders
# where  order_status in ('completed','returned')
# group by datetrunc('month',order_date))

# select month,
# current_month_total,
# lag(current_month_total) over (order by month) as previous_month_amount,
# ((current_month_total- lag(current_month_total) over (order by month))/lag(current_month_total) over (order by month)*100) as mom_growth_percent
# from cte
# """
# ).show()


# # top 10 best selling product so far
# conn.sql(
# """
# with cte as (
# select i.product_id as product_id,  
# sum(o.total_amount) as total_amount
# from
# orders o
# left join order_items i on o.order_id=i.order_id
# where o.order_status ='completed'
# group by i.product_id),

# ranked as (
# select product_id,
# total_amount,
# dense_rank() over(order by total_amount desc) as rnk
# from cte 
# )

# select product_id,
# total_amount,
# from ranked 
# where rnk <=10
# """
# ).show()

# revenue insights



# inventory insights
# for each product what quantity actually get sold monthly 
conn.sql(
"""
select 
i.product_id,
count(i.product_id) as monthly_count,
month(o.order_date) as month
from orders o
left join order_items i on o.order_id=i.order_id
group by 
i.product_id,
month(o.order_date)
order by count(i.product_id) desc
""").show()