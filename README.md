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

