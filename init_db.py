"""
Initialize DuckDB database from CSV files.
Run this script once to set up the database and create all views.
"""

import duckdb
import os
from pathlib import Path

# Database path
DB_PATH = "./db/ecommerce.db"
DATA_DIR = "./data/ecommerce_dataset"

# Create db directory if it doesn't exist
os.makedirs("./db", exist_ok=True)

# Connect to database
conn = duckdb.connect(DB_PATH)

print("📊 Initializing Ecommerce Analytics Database...")
print("=" * 60)

# Load CSV files
csv_files = {
    'users': 'users.csv',
    'products': 'products.csv',
    'orders': 'orders.csv',
    'order_items': 'order_items.csv',
    'reviews': 'reviews.csv',
    'events': 'events.csv'
}

for table_name, csv_file in csv_files.items():
    csv_path = os.path.join(DATA_DIR, csv_file)
    print(f"Loading {table_name}...", end=" ")
    
    try:
        conn.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv_auto('{csv_path}')
        """)
        row_count = conn.sql(f"SELECT COUNT(*) as cnt FROM {table_name}").fetchall()[0][0]
        print(f"✓ ({row_count} rows)")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("📈 Creating analytical views...")
print("=" * 60)

# Create views
views = {
    'daily_revenue': """
        CREATE OR REPLACE VIEW daily_revenue AS
        SELECT
            CAST(o.order_date AS DATE) AS order_date,
            COUNT(o.order_id) as total_orders,
            COUNT(DISTINCT oi.product_id) as products_sold,
            COUNT(DISTINCT o.user_id) as customers_number,
            ROUND(SUM(o.total_amount), 2) as revenue
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY 1
        ORDER BY 1 DESC
    """,
    
    'monthly_growth': """
        CREATE OR REPLACE VIEW monthly_growth AS
        WITH monthly AS (
            SELECT
                DATE_TRUNC('month', order_date)::DATE as month,
                ROUND(SUM(total_amount), 2) as revenue
            FROM orders
            GROUP BY 1
        )
        SELECT
            month,
            revenue,
            LAG(revenue) OVER(ORDER BY month) as prev_revenue,
            ROUND(
                100.0 * (revenue - LAG(revenue) OVER(ORDER BY month)) /
                NULLIF(LAG(revenue) OVER(ORDER BY month), 0),
                2
            ) as mom_growth
        FROM monthly
        ORDER BY month
    """,
    
    'product_performance': """
        CREATE OR REPLACE VIEW product_performance AS
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            SUM(oi.quantity) as units_sold,
            ROUND(SUM(oi.item_total), 2) as revenue,
            ROUND(AVG(p.rating), 2) as avg_rating
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.category, p.rating
        ORDER BY revenue DESC
    """,
    
    'inventory_health': """
        CREATE OR REPLACE VIEW inventory_health AS
        WITH sales AS (
            SELECT
                oi.product_id,
                MIN(o.order_date) as first_sale,
                MAX(o.order_date) as last_sale,
                SUM(oi.quantity) as units_sold
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            GROUP BY oi.product_id
        ),
        velocity AS (
            SELECT
                product_id,
                ROUND(
                    units_sold /
                    NULLIF(DATE_DIFF('day', first_sale, last_sale) + 1, 0),
                    2
                ) AS avg_daily_velocity
            FROM sales
        )
        SELECT
            p.product_id,
            p.product_name,
            COUNT(oi.order_id) as total_orders,
            SUM(oi.quantity) as stock_qty,
            v.avg_daily_velocity
        FROM products p
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        LEFT JOIN velocity v ON p.product_id = v.product_id
        GROUP BY p.product_id, p.product_name, v.avg_daily_velocity
        ORDER BY avg_daily_velocity DESC NULLS LAST
    """,
    
    'customer_cohort': """
        CREATE OR REPLACE VIEW customer_cohort AS
        WITH first_order AS (
            SELECT
                user_id,
                DATE_TRUNC('month', MIN(order_date))::DATE as cohort_month
            FROM orders
            GROUP BY 1
        ),
        activity AS (
            SELECT
                o.user_id,
                DATE_TRUNC('month', o.order_date)::DATE as active_month,
                f.cohort_month
            FROM orders o
            JOIN first_order f ON o.user_id = f.user_id
        )
        SELECT
            cohort_month,
            DATE_DIFF('month', cohort_month, active_month) as month_number,
            COUNT(DISTINCT user_id) as active_users
        FROM activity
        GROUP BY 1, 2
        ORDER BY 1, 2
    """,
    
    'customer_metrics': """
        CREATE OR REPLACE VIEW customer_metrics AS
        WITH customer_orders AS (
            SELECT
                user_id,
                COUNT(*) as order_count,
                ROUND(SUM(total_amount), 2) as total_spent
            FROM orders
            GROUP BY 1
        )
        SELECT
            COUNT(*) as total_customers,
            SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END) as new_customers,
            SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) as returning_customers,
            ROUND(AVG(total_spent), 2) as avg_customer_lifetime_value
        FROM customer_orders
    """
}

for view_name, view_sql in views.items():
    print(f"Creating {view_name}...", end=" ")
    try:
        conn.execute(view_sql)
        print("✓")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("✅ Database initialization complete!")
print(f"📍 Database location: {DB_PATH}")
print("=" * 60)

conn.close()
