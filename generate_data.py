
from faker import Faker
import pandas as pd
import random
import os
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

OUTDIR = "data"
os.makedirs(OUTDIR, exist_ok=True)

N_USERS = 200
N_PRODUCTS = 100
N_ORDERS = 400
MAX_ITEMS_PER_ORDER = 5

# 1) users
users = []
for uid in range(1, N_USERS + 1):
    profile = fake.simple_profile()
    users.append({
        "user_id": uid,
        "username": profile["username"],
        "email": profile["mail"],
        "name": profile["name"],
        "join_date": fake.date_between(start_date="-2y", end_date="today").isoformat()
    })
users_df = pd.DataFrame(users)
users_df.to_csv(f"{OUTDIR}/users.csv", index=False)

# 2) products
categories = ["Electronics", "Home", "Clothing", "Sports", "Beauty", "Books"]
products = []
for pid in range(1, N_PRODUCTS + 1):
    products.append({
        "product_id": pid,
        "name": fake.catch_phrase()[:60],
        "category": random.choice(categories),
        "price": round(random.uniform(5, 500), 2),
        "inventory_count": random.randint(0, 200)
    })
products_df = pd.DataFrame(products)
products_df.to_csv(f"{OUTDIR}/products.csv", index=False)

# 3) orders
orders = []
order_items = []
order_id = 1
for _ in range(N_ORDERS):
    uid = random.randint(1, N_USERS)
    created = fake.date_time_between(start_date="-1y", end_date="now")
    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    total_amount = 0
    for _ in range(num_items):
        pid = random.randint(1, N_PRODUCTS)
        qty = random.randint(1, 3)
        price = products[pid - 1]["price"]
        total_amount += price * qty
        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order_id,
            "product_id": pid,
            "quantity": qty,
            "unit_price": price
        })
    orders.append({
        "order_id": order_id,
        "user_id": uid,
        "order_date": created.isoformat(),
        "total_amount": round(total_amount, 2),
        "status": random.choice(["created", "paid", "shipped", "delivered", "cancelled"])
    })
    order_id += 1

orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)
orders_df.to_csv(f"{OUTDIR}/orders.csv", index=False)
order_items_df.to_csv(f"{OUTDIR}/order_items.csv", index=False)

# 4) reviews (some users review some products)
reviews = []
review_id = 1
for _ in range(int(N_PRODUCTS * 1.5)):
    reviews.append({
        "review_id": review_id,
        "product_id": random.randint(1, N_PRODUCTS),
        "user_id": random.randint(1, N_USERS),
        "rating": random.randint(1, 5),
        "review_text": fake.sentence(nb_words=12),
        "review_date": fake.date_time_between(start_date="-1y", end_date="now").isoformat()
    })
    review_id += 1

reviews_df = pd.DataFrame(reviews)
reviews_df.to_csv(f"{OUTDIR}/reviews.csv", index=False)

print("Generated files in ./data:")
for fn in ["users.csv", "products.csv", "orders.csv", "order_items.csv", "reviews.csv"]:
    print(" -", os.path.join(OUTDIR, fn))