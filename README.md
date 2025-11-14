# ecom-synthetic

This repository contains scripts to generate synthetic e-commerce data (~5 CSV files), ingest them into a SQLite database, and example SQL queries that join multiple tables.

## Files
- `generate_data.py` — generates CSVs in `./data/`
- `ingest_to_sqlite.py` — ingests CSVs into `ecom.db`
- `queries.sql` — example complex join query returning orders in last 30 days with product rating
- `requirements.txt` — Python dependencies
- `.gitignore`

## Quick start
1. Create and activate a Python venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

<---------------------------------------------------------------------------------->

Cursor Prompts Used

These prompts were used inside Cursor to generate the pipeline.

Prompt 1 — Synthetic CSV Generation
You are an assistant that generates Python code to produce synthetic e-commerce CSV files.
Output a single Python script that:
- creates a folder named “data”
- generates the following CSV files with realistic fields:
  1) users.csv: user_id, username, email, name, join_date
  2) products.csv: product_id, name, category, price, inventory_count
  3) orders.csv: order_id, user_id, order_date, total_amount, status
  4) order_items.csv: order_item_id, order_id, product_id, quantity, unit_price
  5) reviews.csv: review_id, product_id, user_id, rating, review_text, review_date
- sizes: ~200 users, ~100 products, ~400 orders, ~150 reviews
- use Faker and pandas
Return only the Python script with no explanation.

Prompt 2 — Ingest CSV Files into SQLite
Generate a Python script that reads CSV files from ./data:
users.csv, products.csv, orders.csv, order_items.csv, reviews.csv
and loads them into a SQLite database file named ecom.db.


Requirements:
- normalize all column names to lowercase with underscores
- create tables: users, products, orders, order_items, reviews
- create indexes on:
  orders(user_id),
  order_items(order_id),
  order_items(product_id),
  reviews(product_id)
- print row counts for each table after loading
Return only the Python script, without explanation.
Prompt 3 — Multi‑Table SQL Join Query
