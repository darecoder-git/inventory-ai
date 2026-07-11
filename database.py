import duckdb

DB_PATH = "./db/ecommerce.db"

def get_connection():
    """Get a DuckDB connection to the ecommerce database."""
    return duckdb.connect(DB_PATH)