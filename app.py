from dash import Dash
from dash import html
from dash import dcc

import dash_bootstrap_components as dbc
from pages.overview import overview_page
# from pages.sales import sales_page
# from pages.inventory import inventory_page
# from pages.customers import customers_page



app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG
    ]
)

app.layout = dbc.Container([

    html.H1(
        "Shopify Merchant Dashboard"
    ),

    dbc.Tabs([

        dbc.Tab(
            overview_page(),
            label="Overview"
        ),

            # dbc.Tab(
            #      sales_page(),
            #     label="Sales"
            # ),

            # dbc.Tab(
            #     inventory_page(),
            #     label="Inventory"
            # ),

            # dbc.Tab(
            #     customers_page(),
            #     label="Customers"
            # )

    ])

], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)