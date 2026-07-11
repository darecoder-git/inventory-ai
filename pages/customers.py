from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from database import get_connection


def customers_page():
    con = get_connection()

    # Customer metrics
    metrics = con.sql("""
        SELECT *
        FROM customer_metrics
    """).df()

    total_customers = metrics.total_customers[0] if metrics.total_customers[0] else 0
    new_customers = metrics.new_customers[0] if metrics.new_customers[0] else 0
    returning_customers = metrics.returning_customers[0] if metrics.returning_customers[0] else 0
    clv = metrics.avg_customer_lifetime_value[0] if metrics.avg_customer_lifetime_value[0] else 0

    # Customer distribution pie
    customer_dist = con.sql("""
        SELECT
            CASE
                WHEN order_count = 1 THEN 'New Customers'
                ELSE 'Returning Customers'
            END as customer_type,
            COUNT(*) as count
        FROM (
            SELECT user_id, COUNT(*) as order_count
            FROM orders
            GROUP BY user_id
        )
        GROUP BY 1
    """).df()

    dist_fig = px.pie(
        customer_dist,
        values="count",
        names="customer_type",
        title="Customer Segmentation"
    )

    # Customer spending distribution
    spending_dist = con.sql("""
        SELECT
            CASE
                WHEN total_spent < 100 THEN '$0-100'
                WHEN total_spent < 500 THEN '$100-500'
                WHEN total_spent < 1000 THEN '$500-1000'
                ELSE '$1000+'
            END as spending_bracket,
            COUNT(*) as customer_count
        FROM (
            SELECT user_id, SUM(total_amount) as total_spent
            FROM orders
            GROUP BY user_id
        )
        GROUP BY 1
        ORDER BY spending_bracket
    """).df()

    spending_fig = px.bar(
        spending_dist,
        x="spending_bracket",
        y="customer_count",
        title="Customer Spending Distribution",
        labels={"customer_count": "Number of Customers", "spending_bracket": "Spending Bracket"}
    )

    # Top customers
    top_customers = con.sql("""
        SELECT
            u.user_id,
            u.name,
            COUNT(o.order_id) as total_orders,
            ROUND(SUM(o.total_amount), 2) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.user_id = o.user_id
        GROUP BY u.user_id, u.name
        ORDER BY total_spent DESC
        LIMIT 15
    """).df()

    return html.Div([
        # KPI Cards
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Customers", className="text-muted"),
                        html.H2(int(total_customers), className="text-success")
                    ])
                ], className="mb-3")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("New Customers", className="text-muted"),
                        html.H2(int(new_customers), className="text-info")
                    ])
                ], className="mb-3")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Returning Customers", className="text-muted"),
                        html.H2(int(returning_customers), className="text-warning")
                    ])
                ], className="mb-3")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Avg Customer LTV", className="text-muted"),
                        html.H2(f"${clv:,.2f}", className="text-danger")
                    ])
                ], className="mb-3")
            ),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=dist_fig),
                width=6
            ),
            dbc.Col(
                dcc.Graph(figure=spending_fig),
                width=6
            )
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.H5("Top Customers"),
                dbc.Table.from_dataframe(
                    top_customers,
                    striped=True,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    size="sm"
                )
            ])
        ])
    ])
