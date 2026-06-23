top_products=con.sql("""
SELECT *
FROM product_performance
ORDER BY revenue DESC
LIMIT 10
""").df()

product_fig=px.bar(
    top_products,
    x="revenue",
    y="product_name",
    orientation="h"
)