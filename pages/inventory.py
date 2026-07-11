from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from database import get_connection


def inventory_page():
    con = get_connection()

    # Inventory health data
    inventory = con.sql("""
        SELECT *
        FROM inventory_health
        WHERE avg_daily_velocity > 0
        ORDER BY avg_daily_velocity DESC
        LIMIT 20
    """).df()

    # Chart for daily velocity
    velocity_fig = px.bar(
        inventory,
        x="product_name",
        y="avg_daily_velocity",
        title="Top 20 Products by Daily Velocity",
        labels={"avg_daily_velocity": "Avg Daily Velocity", "product_name": "Product"}
    )
    velocity_fig.update_layout(xaxis_tickangle=-45)

    # Sales velocity heatmap
    velocity_scatter = px.scatter(
        inventory,
        x="stock_qty",
        y="avg_daily_velocity",
        size="total_orders",
        hover_data={"product_name": True},
        title="Inventory Health: Stock vs Velocity",
        labels={"stock_qty": "Total Orders", "avg_daily_velocity": "Daily Velocity"}
    )

    # Critical inventory (low velocity items)
    critical_inventory = con.sql("""
        SELECT
            product_name,
            total_orders,
            avg_daily_velocity,
            stock_qty
        FROM inventory_health
        WHERE avg_daily_velocity > 0
        ORDER BY avg_daily_velocity ASC
        LIMIT 15
    """).df()

    return html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=velocity_fig),
                width=12
            )
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=velocity_scatter),
                width=12
            )
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.H5("Slow Moving Inventory"),
                dbc.Alert(
                    "These products have low daily velocity and may need attention",
                    color="warning"
                ),
                dbc.Table.from_dataframe(
                    critical_inventory,
                    striped=True,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    size="sm"
                )
            ])
        ])
    ])
