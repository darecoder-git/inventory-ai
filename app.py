"""
Ecommerce Analytics Dashboard
Multi-page Dash application for analyzing ecommerce metrics
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from pages.overview import overview_page
from pages.sales import sales_page
from pages.inventory import inventory_page
from pages.customers import customers_page
from pages.forecasting import forecasting_page
from pages.cohort import cohort_page

# Initialize app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG]
)

app.title = "Ecommerce Analytics Dashboard"

# Define layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1(
                "📊 Ecommerce Analytics Dashboard",
                className="mb-4 mt-4"
            )
        ])
    ]),

    dbc.Tabs([
        dbc.Tab(
            overview_page(),
            label="📈 Overview",
            className="p-4"
        ),
        dbc.Tab(
            sales_page(),
            label="💰 Sales",
            className="p-4"
        ),
        dbc.Tab(
            inventory_page(),
            label="📦 Inventory",
            className="p-4"
        ),
        dbc.Tab(
            customers_page(),
            label="👥 Customers",
            className="p-4"
        ),
        dbc.Tab(
            forecasting_page(),
            label="🔮 Forecasting",
            className="p-4"
        ),
        dbc.Tab(
            cohort_page(),
            label="📊 Cohort Analysis",
            className="p-4"
        ),
    ], id="tabs")

], fluid=True, className="p-0")

if __name__ == "__main__":
    app.run(debug=True)
