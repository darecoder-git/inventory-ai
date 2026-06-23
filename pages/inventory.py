inventory=con.sql("""
SELECT *
FROM inventory_health
ORDER BY days_remaining
LIMIT 20
""").df()

inventory_fig=px.bar(
    inventory,
    x="product_id",
    y="days_remaining"
)


critical=inventory[
    inventory.days_remaining < 7
]