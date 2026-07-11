from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from database import get_connection


def overview_page():
    con = get_connection()

    # Get KPIs
    kpis = con.sql("""
        SELECT
            SUM(total_amount) as revenue,
            COUNT(*) as orders,
            COUNT(DISTINCT user_id) as customers,
            ROUND(SUM(total_amount)/COUNT(*), 2) as aov
        FROM orders
    """).df()

    # Get daily revenue trend
    revenue_trend = con.sql("""
        SELECT *
        FROM daily_revenue
        ORDER BY order_date DESC
        LIMIT 30
    """).df()

    revenue_fig = px.line(
        revenue_trend.sort_values('order_date'),
        x="order_date",
        y="revenue",
        title="Daily Revenue Trend",
        labels={"revenue": "Revenue ($)", "order_date": "Date"}
    )

    # Get recent orders
    recent_orders = con.sql("""
        SELECT
            o.order_id,
            o.user_id,
            COUNT(oi.product_id) as items,
            o.total_amount,
            o.order_status,
            o.order_date
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY o.order_id, o.user_id, o.total_amount, o.order_status, o.order_date
        ORDER BY o.order_date DESC
        LIMIT 10
    """).df()

    revenue_val = kpis.revenue[0] if kpis.revenue[0] else 0
    orders_val = kpis.orders[0] if kpis.orders[0] else 0
    customers_val = kpis.customers[0] if kpis.customers[0] else 0
    aov_val = kpis.aov[0] if kpis.aov[0] else 0

    return html.Div([
        # KPI Cards
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Revenue", className="text-muted"),
                        html.H2(f"${revenue_val:,.2f}", className="text-success")
                    ])
                ], className="mb-3")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Orders", className="text-muted"),
                        html.H2(int(orders_val), className="text-info")
                    ])
                ], className="mb-3")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Customers", className="text-muted"),
                        html.H2(int(customers_val), className="text-warning")
                    ])
                ], className="mb-3")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Avg Order Value", className="text-muted"),
                        html.H2(f"${aov_val:,.2f}", className="text-danger")
                    ])
                ], className="mb-3")
            ),
        ], className="mb-4"),

        # Revenue Trend Chart
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=revenue_fig),
                width=12
            )
        ], className="mb-4"),

        # Recent Orders Table
        dbc.Row([
            dbc.Col([
                html.H5("Recent Orders"),
                dbc.Table.from_dataframe(
                    recent_orders,
                    striped=True,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    size="sm"
                )
            ])
        ])
    ])
