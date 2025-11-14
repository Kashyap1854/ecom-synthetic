
import pandas as pd
import sqlite3
import os

DB_PATH = "ecom.db"
DATA_DIR = "data"

tables = {
    "users": os.path.join(DATA_DIR, "users.csv"),
    "products": os.path.join(DATA_DIR, "products.csv"),
    "orders": os.path.join(DATA_DIR, "orders.csv"),
    "order_items": os.path.join(DATA_DIR, "order_items.csv"),
    "reviews": os.path.join(DATA_DIR, "reviews.csv"),
}

conn = sqlite3.connect(DB_PATH)
for table_name, csv_path in tables.items():
    print(f"Loading {csv_path} into {table_name} ...")
    df = pd.read_csv(csv_path)
    # Ensure column names are SQL-friendly
    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f" - {table_name}: {len(df)} rows")

# Create some indexes for join performance
cur = conn.cursor()
cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_orderitems_order ON order_items(order_id);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_orderitems_product ON order_items(product_id);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);")
conn.commit()
conn.close()
print("Ingestion complete. DB file:", DB_PATH)