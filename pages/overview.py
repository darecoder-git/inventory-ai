from dash import html,dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from database import get_connection



def overview_page():
    con=get_connection()

    kpis=con.sql("""

    SELECT
        SUM(total_amount) revenue,
        COUNT(*) orders,
        COUNT(DISTINCT user_id) customers,
        ROUND(
            SUM(total_amount)/COUNT(*),
            2
        ) aov

    FROM orders

    """).df()

    revenue_fig=px.line(
        con.sql("""
        SELECT *
        FROM daily_revenue
        LIMIT 100
        """).df(),
        x="order_date",
        y="revenue"
    )

    return html.Div([

        dbc.Row([

            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Revenue"),
                        html.H2(f"${kpis.revenue[0]:,.0f}")
                    ])
                ])
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Orders"),
                        html.H2(kpis.orders)
                    ])
                ])
            )

        ]),

        dcc.Graph(
            figure=revenue_fig
        )

    ])