from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from database import get_connection


def sales_page():
    con = get_connection()

    # Monthly growth
    monthly_growth = con.sql("""
        SELECT *
        FROM monthly_growth
        ORDER BY month
    """).df()

    growth_fig = px.bar(
        monthly_growth,
        x="month",
        y="revenue",
        title="Monthly Revenue",
        labels={"revenue": "Revenue ($)", "month": "Month"},
        color="mom_growth",
        color_continuous_scale="RdYlGn",
        hover_data={"mom_growth": ":.2f"}
    )

    # Top products
    top_products = con.sql("""
        SELECT *
        FROM product_performance
        ORDER BY revenue DESC
        LIMIT 10
    """).df()

    product_fig = px.bar(
        top_products,
        x="revenue",
        y="product_name",
        orientation="h",
        title="Top 10 Products by Revenue",
        labels={"revenue": "Revenue ($)", "product_name": "Product"},
        color="units_sold",
        color_continuous_scale="Viridis"
    )

    # Category breakdown
    category_sales = con.sql("""
        SELECT
            category,
            ROUND(SUM(revenue), 2) as total_revenue,
            SUM(units_sold) as total_units
        FROM product_performance
        GROUP BY category
        ORDER BY total_revenue DESC
    """).df()

    category_fig = px.pie(
        category_sales,
        values="total_revenue",
        names="category",
        title="Revenue by Category"
    )

    return html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=growth_fig),
                width=12
            )
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=product_fig),
                width=8
            ),
            dbc.Col(
                dcc.Graph(figure=category_fig),
                width=4
            )
        ]),

        dbc.Row([
            dbc.Col([
                html.H5("Product Performance"),
                dbc.Table.from_dataframe(
                    top_products.head(10),
                    striped=True,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    size="sm"
                )
            ])
        ])
    ])
