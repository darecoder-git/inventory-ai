# 📊 Ecommerce Analytics Dashboard

A comprehensive analytics dashboard for e-commerce businesses built with **Dash**, **DuckDB**, and **Python**.

## Features

- **📈 Overview Dashboard** - Key metrics, revenue trends, and recent orders
- **💰 Sales Analytics** - Monthly growth, top products, category breakdown
- **📦 Inventory Management** - Product velocity, stock analysis, slow-moving items
- **👥 Customer Insights** - Segmentation, spending patterns, customer lifetime value
- **🔮 Time Series Forecasting** - 30-day revenue forecasts using Prophet
- **📊 Cohort Analysis** - Retention heatmaps and customer lifetime tracking

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

The database is loaded from CSV files in `data/ecommerce_dataset/`. Run the initialization script:

```bash
python init_db.py
```

This will:
- Load CSV data into DuckDB
- Create all analytical views
- Build the database at `db/ecommerce.db`

### 3. Run the Dashboard

```bash
python app.py
```

The dashboard will be available at **http://localhost:8050**

## Project Structure

```
ecommerce-analytics-dashboard/
├── app.py                          # Main Dash application
├── database.py                     # Database connection utilities
├── init_db.py                      # Database initialization script
├── requirements.txt                # Python dependencies
│
├── pages/                          # Multi-page components
│   ├── overview.py                # Dashboard overview
│   ├── sales.py                   # Sales analytics
│   ├── inventory.py               # Inventory management
│   ├── customers.py               # Customer insights
│   ├── forecasting.py             # Revenue forecasting
│   └── cohort.py                  # Cohort analysis
│
├── data/
│   └── ecommerce_dataset/         # CSV source data
│       ├── users.csv
│       ├── orders.csv
│       ├── order_items.csv
│       ├── products.csv
│       ├── reviews.csv
│       └── events.csv
│
├── db/                            # DuckDB database
│   └── ecommerce.db
│
└── assets/
    └── style.css                 # Custom styling
```

## Database Schema

### Tables

- **users** - Customer information
- **products** - Product catalog with ratings
- **orders** - Order details and totals
- **order_items** - Line items in each order
- **reviews** - Customer product reviews
- **events** - Customer behavior events (cart, view, purchase, etc.)

### Views

- **daily_revenue** - Daily sales metrics
- **monthly_growth** - Month-over-month growth rates
- **product_performance** - Product sales and revenue analysis
- **inventory_health** - Product velocity and sales frequency
- **customer_cohort** - Customer retention by cohort
- **customer_metrics** - Aggregate customer statistics

## Development

### Adding a New Page

1. Create a new file in `pages/` directory
2. Define a page function that returns a Dash HTML component
3. Import and add a tab to `app.py`

Example:

```python
# pages/new_page.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from database import get_connection

def new_page():
    con = get_connection()
    # Your analytics here
    return html.Div([...])
```

### Running Tests

To verify the database has been initialized correctly:

```bash
python -c "from database import get_connection; con = get_connection(); print(con.execute('SELECT COUNT(*) FROM orders').fetchall())"
```

## Dependencies

- **dash** - Web framework
- **plotly** - Interactive visualizations
- **duckdb** - In-process SQL database
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **prophet** - Time series forecasting (optional)

## Notes

- The dashboard uses DuckDB for fast SQL queries on CSV data
- All data is loaded into memory for quick performance
- The Prophet forecasting model requires historical data to make accurate predictions
- For production use, consider using a proper database backend

## Future Enhancements

- [ ] Real-time data sync
- [ ] Custom date range filters
- [ ] Export reports to PDF
- [ ] User authentication
- [ ] Database backend (PostgreSQL, MySQL)
- [ ] API integration
