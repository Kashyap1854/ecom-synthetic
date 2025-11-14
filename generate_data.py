
import os
import random
from datetime import datetime
from faker import Faker
import pandas as pd

fake = Faker()
random.seed(42)
Faker.seed(42)

DATA_DIR = "data"
USER_COUNT = 200
PRODUCT_COUNT = 100
ORDER_COUNT = 400
REVIEW_COUNT = 150

os.makedirs(DATA_DIR, exist_ok=True)

def generate_users(n):
    users = []
    for user_id in range(1, n + 1):
        name = fake.name()
        username = fake.user_name()
        email = fake.email()
        join_date = fake.date_between(start_date="-2y", end_date="today").isoformat()
        users.append(
            dict(
                user_id=user_id,
                username=username,
                email=email,
                name=name,
                join_date=join_date,
            )
        )
    return pd.DataFrame(users)

def generate_products(n):
    categories = ["Electronics", "Home", "Beauty", "Sports", "Fashion", "Books"]
    products = []
    for product_id in range(1, n + 1):
        name = fake.catch_phrase()
        category = random.choice(categories)
        price = round(random.uniform(5, 500), 2)
        inventory_count = random.randint(0, 1000)
        products.append(
            dict(
                product_id=product_id,
                name=name,
                category=category,
                price=price,
                inventory_count=inventory_count,
            )
        )
    return pd.DataFrame(products)

def generate_orders(n, user_ids):
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    orders = []
    for order_id in range(1, n + 1):
        user_id = random.choice(user_ids)
        order_date = fake.date_time_between(start_date="-1y", end_date="now").isoformat()
        total_amount = round(random.uniform(20, 1500), 2)
        status = random.choice(statuses)
        orders.append(
            dict(
                order_id=order_id,
                user_id=user_id,
                order_date=order_date,
                total_amount=total_amount,
                status=status,
            )
        )
    return pd.DataFrame(orders)

def generate_order_items(orders_df, products_df):
    order_items = []
    order_item_id = 1
    for _, order in orders_df.iterrows():
        num_items = random.randint(1, 5)
        product_choices = random.sample(list(products_df["product_id"]), k=num_items)
        for product_id in product_choices:
            quantity = random.randint(1, 5)
            unit_price = float(
                products_df.loc[products_df["product_id"] == product_id, "price"].iloc[0]
            )
            order_items.append(
                dict(
                    order_item_id=order_item_id,
                    order_id=int(order["order_id"]),
                    product_id=int(product_id),
                    quantity=quantity,
                    unit_price=unit_price,
                )
            )
            order_item_id += 1
    return pd.DataFrame(order_items)

def generate_reviews(n, product_ids, user_ids):
    reviews = []
    for review_id in range(1, n + 1):
        product_id = random.choice(product_ids)
        user_id = random.choice(user_ids)
        rating = random.randint(1, 5)
        review_text = fake.paragraph(nb_sentences=3)
        review_date = fake.date_between(start_date="-1y", end_date="today").isoformat()
        reviews.append(
            dict(
                review_id=review_id,
                product_id=product_id,
                user_id=user_id,
                rating=rating,
                review_text=review_text,
                review_date=review_date,
            )
        )
    return pd.DataFrame(reviews)

users_df = generate_users(USER_COUNT)
products_df = generate_products(PRODUCT_COUNT)
orders_df = generate_orders(ORDER_COUNT, list(users_df["user_id"]))
order_items_df = generate_order_items(orders_df, products_df)
reviews_df = generate_reviews(REVIEW_COUNT, list(products_df["product_id"]), list(users_df["user_id"]))

file_map = {
    "users.csv": users_df,
    "products.csv": products_df,
    "orders.csv": orders_df,
    "order_items.csv": order_items_df,
    "reviews.csv": reviews_df,
}

saved_paths = []
for filename, df in file_map.items():
    path = os.path.join(DATA_DIR, filename)
    df.to_csv(path, index=False)
    saved_paths.append(path)

print("Generated files:")
for path in saved_paths:
    print(path)
