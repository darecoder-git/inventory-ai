from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from database import get_connection
import numpy as np


def cohort_page():
    con = get_connection()

    # Get cohort analysis data
    cohort_data = con.sql("""
        SELECT *
        FROM customer_cohort
        WHERE month_number IS NOT NULL
        ORDER BY cohort_month, month_number
    """).df()

    if len(cohort_data) == 0:
        return html.Div([
            dbc.Alert("Not enough data for cohort analysis yet", color="info")
        ])

    # Pivot for heatmap
    pivot = cohort_data.pivot_table(
        index="cohort_month",
        columns="month_number",
        values="active_users"
    )

    # Create heatmap
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index.astype(str),
        colorscale="Blues",
        hovertemplate="Cohort: %{y}<br>Month: %{x}<br>Active Users: %{z}<extra></extra>"
    ))

    heatmap_fig.update_layout(
        title="Customer Cohort Retention Heatmap",
        xaxis_title="Months Since First Purchase",
        yaxis_title="Cohort Month"
    )

    # Retention rate analysis
    retention_rate = cohort_data.copy()
    retention_rate["retention_pct"] = retention_rate.groupby("cohort_month")["active_users"].transform(
        lambda x: (x / x.iloc[0] * 100).round(2) if x.iloc[0] > 0 else 0
    )

    # Get average retention curve
    avg_retention = retention_rate.groupby("month_number")["retention_pct"].mean().reset_index()
    
    retention_fig = px.line(
        avg_retention,
        x="month_number",
        y="retention_pct",
        markers=True,
        title="Average Retention Curve",
        labels={"retention_pct": "Retention Rate (%)", "month_number": "Months Since First Purchase"}
    )
    retention_fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="50% Retention")

    # Cohort size
    cohort_size = con.sql("""
        WITH first_purchase AS (
            SELECT
                user_id,
                DATE_TRUNC('month', MIN(order_date))::DATE as cohort_month
            FROM orders
            GROUP BY user_id
        )
        SELECT
            cohort_month,
            COUNT(DISTINCT user_id) as cohort_size
        FROM first_purchase
        GROUP BY 1
        ORDER BY 1
    """).df()

    size_fig = px.bar(
        cohort_size,
        x="cohort_month",
        y="cohort_size",
        title="Cohort Size Over Time",
        labels={"cohort_size": "Number of Customers", "cohort_month": "Cohort Month"}
    )

    return html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=heatmap_fig),
                width=12
            )
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=retention_fig),
                width=6
            ),
            dbc.Col(
                dcc.Graph(figure=size_fig),
                width=6
            )
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.H5("Cohort Analysis Guide"),
                dbc.Card([
                    dbc.CardBody([
                        html.P("The heatmap shows customer retention over time:"),
                        html.Ul([
                            html.Li("Rows: Customer cohorts (grouped by first purchase month)"),
                            html.Li("Columns: Months since first purchase"),
                            html.Li("Darker colors: Higher retention rates"),
                            html.Li("Use this to identify patterns in customer retention")
                        ])
                    ])
                ])
            ])
        ])
    ])
