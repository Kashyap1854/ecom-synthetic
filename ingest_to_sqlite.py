
import os
import sqlite3
import pandas as pd

DATA_DIR = "./data"
DB_PATH = "ecom.db"
TABLE_FILES = {
    "users": "users.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "reviews": "reviews.csv",
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df

def load_csvs():
    dataframes = {}
    for table, filename in TABLE_FILES.items():
        path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(path)
        dataframes[table] = normalize_columns(df)
    return dataframes

def write_to_sqlite(dfs):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        for table, df in dfs.items():
            df.to_sql(table, conn, if_exists="replace", index=False)
        with conn:
            conn.execute("CREATE INDEX idx_orders_user_id ON orders(user_id)")
            conn.execute("CREATE INDEX idx_order_items_order_id ON order_items(order_id)")
            conn.execute("CREATE INDEX idx_order_items_product_id ON order_items(product_id)")
            conn.execute("CREATE INDEX idx_reviews_product_id ON reviews(product_id)")
    finally:
        conn.close()

def print_counts():
    conn = sqlite3.connect(DB_PATH)
    try:
        for table in TABLE_FILES.keys():
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count}")
    finally:
        conn.close()

def main():
    dfs = load_csvs()
    write_to_sqlite(dfs)
    print_counts()
    print(f"Database path: {os.path.abspath(DB_PATH)}")

if __name__ == "__main__":
    main()
