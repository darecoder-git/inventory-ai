import duckdb

DB_PATH = "./db/business_db.db"

def get_connection():
    return duckdb.connect(DB_PATH)