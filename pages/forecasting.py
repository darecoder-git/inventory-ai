from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from database import get_connection
import pandas as pd

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False


def forecasting_page():
    con = get_connection()

    # Get daily revenue for forecasting
    daily_data = con.sql("""
        SELECT
            order_date,
            revenue
        FROM daily_revenue
        ORDER BY order_date DESC
        LIMIT 90
    """).df()

    daily_data = daily_data.sort_values('order_date')

    # Create base chart with historical data
    historical_fig = px.line(
        daily_data,
        x="order_date",
        y="revenue",
        title="Historical Daily Revenue",
        labels={"revenue": "Revenue ($)", "order_date": "Date"}
    )

    forecast_content = []

    if PROPHET_AVAILABLE and len(daily_data) > 10:
        try:
            # Prepare data for Prophet
            df_prophet = daily_data.copy()
            df_prophet.columns = ["ds", "y"]
            df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])
            df_prophet = df_prophet.sort_values("ds")

            # Train model
            model = Prophet(yearly_seasonality=False, weekly_seasonality=True)
            model.fit(df_prophet)

            # Make future dataframe
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)

            # Create forecast figure
            forecast_fig = go.Figure()
            
            # Add historical data
            forecast_fig.add_trace(go.Scatter(
                x=df_prophet["ds"],
                y=df_prophet["y"],
                mode="lines",
                name="Historical",
                line=dict(color="blue")
            ))

            # Add forecast
            forecast_fig.add_trace(go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat"],
                mode="lines",
                name="Forecast",
                line=dict(color="red", dash="dash")
            ))

            # Add confidence interval
            forecast_fig.add_trace(go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_upper"],
                mode="lines",
                name="Upper Bound",
                line=dict(width=0),
                showlegend=False
            ))

            forecast_fig.add_trace(go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_lower"],
                mode="lines",
                name="Lower Bound",
                line=dict(width=0),
                fillcolor="rgba(255,0,0,0.1)",
                fill="tonexty",
                showlegend=False
            ))

            forecast_fig.update_layout(
                title="30-Day Revenue Forecast",
                xaxis_title="Date",
                yaxis_title="Revenue ($)",
                hovermode="x unified"
            )

            forecast_content = [
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(figure=forecast_fig),
                        width=12
                    )
                ], className="mb-4"),
                dbc.Row([
                    dbc.Col(
                        dbc.Alert(
                            "✓ Forecast generated using Prophet time series model",
                            color="success"
                        )
                    )
                ])
            ]
        except Exception as e:
            forecast_content = [
                dbc.Row([
                    dbc.Col(
                        dbc.Alert(f"Error generating forecast: {str(e)}", color="danger")
                    )
                ])
            ]
    else:
        forecast_content = [
            dbc.Row([
                dbc.Col(
                    dbc.Alert(
                        "⚠️ Prophet not available or insufficient data for forecasting. "
                        "Install Prophet with: pip install prophet",
                        color="warning"
                    )
                )
            ])
        ]

    return html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=historical_fig),
                width=12
            )
        ], className="mb-4"),
    ] + forecast_content)
