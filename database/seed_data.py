import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import sys

fake = Faker()

DB_CONFIG = {
    "dbname": "retail_analytics",
    "user": "analyst",
    "password": "analyst_pass",
    "host": "localhost",
    "port": "5433"
}

def seed_database():
    print("🔌 Connecting to database...", flush=True)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # 🧹 Clear existing data to prevent duplicate key errors
        print("🧹 Clearing old data...", flush=True)
        cur.execute("TRUNCATE transaction_items, transactions, products, customers CASCADE;")
        conn.commit()
        print("✅ Tables cleared.", flush=True)
        
        # 1. Seed Customers
        print("👥 Seeding 50 customers...", flush=True)
        customers = [(fake.email(), fake.first_name(), fake.last_name(), fake.country()) for _ in range(50)]
        cur.executemany(
            "INSERT INTO customers (email, first_name, last_name, country) VALUES (%s, %s, %s, %s)",
            customers
        )
        conn.commit()
        
        cur.execute("SELECT customer_id FROM customers")
        customer_ids = [row[0] for row in cur.fetchall()]
        
        # 2. Seed Products
        print("📦 Seeding 50 products...", flush=True)
        categories = ["Electronics", "Apparel", "Home & Garden", "Sports", "Books"]
        products = []
        for cat in categories:
            for i in range(10):
                cost = round(random.uniform(10, 200), 2)
                price = round(cost * random.uniform(1.2, 2.5), 2)
                products.append((f"{cat[:3].upper()}-{i+1:03d}", f"{cat} Item {i+1}", cat, cost, price))
        cur.executemany(
            "INSERT INTO products (sku, name, category, unit_cost, unit_price) VALUES (%s, %s, %s, %s, %s)",
            products
        )
        conn.commit()
        
        # Pre-fetch prices to avoid 600+ redundant queries
        cur.execute("SELECT product_id, unit_price FROM products")
        product_prices = {row[0]: row[1] for row in cur.fetchall()}
        product_ids = list(product_prices.keys())
        
        # 3. Seed Transactions & Line Items
        print("💳 Seeding ~300 transactions...", flush=True)
        for _ in range(300):
            t_date = datetime.now() - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
            cur.execute(
                "INSERT INTO transactions (customer_id, transaction_date, status, payment_method) "
                "VALUES (%s, %s, 'completed', %s) RETURNING transaction_id",
                (random.choice(customer_ids), t_date, random.choice(["credit_card", "paypal", "debit_card"]))
            )
            t_id = cur.fetchone()[0]
            
            # 1-3 items per transaction
            for _ in range(random.randint(1, 3)):
                prod_id = random.choice(product_ids)
                price = product_prices[prod_id]  # ✅ Fast dict lookup
                qty = random.randint(1, 5)
                cur.execute(
                    "INSERT INTO transaction_items (transaction_id, product_id, quantity, unit_price) "
                    "VALUES (%s, %s, %s, %s)",
                    (t_id, prod_id, qty, price)
                )
        conn.commit()
        print("✅ Seeding complete! Loaded 50 customers, 50 products, ~300 transactions.", flush=True)
        
    except Exception as e:
        conn.rollback()
        print(f"❌ CRASH: {e}", flush=True)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_database()