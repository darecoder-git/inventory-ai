shopify_dashboard/

data/
├── customers.csv
├── orders.csv
├── order_items.csv
├── products.csv

db/
└── ecommerce.duckdb

sql/
├── 01_daily_sales.sql
├── 02_monthly_growth.sql
├── 03_product_performance.sql
├── 04_inventory_health.sql
├── 05_customer_metrics.sql
├── 06_cohort_retention.sql

dashboard/
├── app.py
├── database.py
├── pages/
│   ├── overview.py
│   ├── sales.py
│   ├── inventory.py
│   ├── customers.py
│   └── forecasting.py
└── assets/
    └── style.css