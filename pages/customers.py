SELECT *
FROM customer_metrics

fig=px.pie(
    names=[
        "New",
        "Returning"
    ],
    values=[
        new_count,
        return_count
    ]
)