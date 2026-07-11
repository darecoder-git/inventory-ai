# Setup Instructions

## Prerequisites

- Python 3.10+
- pip (Python package manager)

## Installation

### 1. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python3 init_db.py
```

This will:
- Load CSV data from `data/ecommerce_dataset/`
- Create DuckDB database at `db/ecommerce.db`
- Build all analytical views automatically

## Running the Dashboard

### Option 1: Using the startup script

```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual startup

```bash
source venv/bin/activate
python3 app.py
```

### Option 3: Using Python directly

```bash
source venv/bin/activate
python3 -m flask run --app app:app
```

Then visit: **http://localhost:8050**

## Verify Installation

```bash
# Test database connection
python3 -c "from database import get_connection; con = get_connection(); print(con.execute('SELECT COUNT(*) FROM orders').fetchall())"

# Test app import
python3 -c "from app import app; print('✅ App loaded successfully')"
```

## Project Structure

```
Inventory-AI/
├── app.py                    # Main Dash application
├── database.py              # DuckDB connection utilities
├── init_db.py               # Database initialization
├── requirements.txt         # Dependencies
├── run.sh                   # Startup script
│
├── pages/                   # Dashboard pages
│   ├── overview.py         # Key metrics and trends
│   ├── sales.py            # Sales analytics
│   ├── inventory.py        # Inventory management
│   ├── customers.py        # Customer insights
│   ├── forecasting.py      # Revenue forecasting
│   └── cohort.py           # Cohort retention analysis
│
├── data/ecommerce_dataset/  # Source CSV files
│   ├── users.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── reviews.csv
│   └── events.csv
│
└── db/                      # DuckDB database
    └── ecommerce.db
```

## Dashboard Pages

1. **📈 Overview** - Executive summary with KPIs
2. **💰 Sales** - Revenue analysis and trends
3. **📦 Inventory** - Product velocity and stock analysis
4. **👥 Customers** - Segmentation and lifetime value
5. **🔮 Forecasting** - 30-day revenue forecast (requires Prophet)
6. **📊 Cohort Analysis** - Retention and customer journey

## Troubleshooting

### Database already exists
```bash
rm db/ecommerce.db
python3 init_db.py
```

### Module not found errors
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Port 8050 already in use
Edit `app.py` and change the port:
```python
app.run(debug=True, port=8051)
```

### Prophet forecasting not working
Install Prophet separately:
```bash
pip install prophet
```

## Next Steps

- Customize the dashboard styling in `assets/style.css`
- Add new SQL views to `init_db.py`
- Create additional analysis pages in `pages/`
- Connect to a real database backend for production

## Support

For issues or questions, refer to:
- [Dash Documentation](https://dash.plotly.com/)
- [DuckDB Documentation](https://duckdb.org/)
- [Plotly Documentation](https://plotly.com/python/)
