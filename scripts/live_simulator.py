import requests, time, random, logging, sys
import psycopg2

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", force=True)

API_URL = "http://localhost:8000/api/v1/data/ingest"
DB_CONFIG = {
    "dbname": "retail_analytics",
    "user": "analyst",
    "password": "analyst_pass",
    "host": "localhost",
    "port": "5433"
}

def fetch_valid_ids():
    """Fetch real UUIDs from database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT customer_id FROM customers LIMIT 50")
        customers = [str(row[0]) for row in cur.fetchall()]
        cur.execute("SELECT product_id FROM products LIMIT 50")
        products = [str(row[0]) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return customers, products
    except Exception as e:
        logging.error(f"DB fetch failed: {e}")
        return [], []

# Initial ID fetch
logging.info("🔄 Fetching valid IDs from database...")
CUSTOMER_IDS, PRODUCT_IDS = fetch_valid_ids()

if not CUSTOMER_IDS or not PRODUCT_IDS:
    logging.error("❌ Database empty or unreachable. Run 'python database/seed_data.py' first.")
    sys.exit(1)

logging.info(f"✅ Loaded {len(CUSTOMER_IDS)} customers & {len(PRODUCT_IDS)} products")

def simulate_transaction():
    """Generate realistic transaction payload"""
    k = random.randint(1, min(3, len(PRODUCT_IDS)))
    return {
        "customer_id": random.choice(CUSTOMER_IDS),
        "product_ids": random.sample(PRODUCT_IDS, k),
        "quantities": [random.randint(1, 4) for _ in range(k)],
        "payment_method": random.choice(["credit_card", "paypal", "debit_card"])
    }

logging.info("🚀 Starting live transaction simulator (Ctrl+C to stop)...")
retry_count = 0

while True:
    try:
        # Re-fetch IDs every 10 cycles in case DB was reseeded
        if retry_count % 10 == 0:
            CUSTOMER_IDS, PRODUCT_IDS = fetch_valid_ids()
        
        payload = simulate_transaction()
        resp = requests.post(API_URL, json=payload, timeout=10)
        
        if resp.status_code == 201:
            logging.info(f"✅ Ingested: {resp.json()['transaction_id']}")
            retry_count = 0  # Reset on success
        elif resp.status_code == 400:
            logging.warning(f"⚠️ Bad request: {resp.text[:100]}")
        elif resp.status_code == 500:
            logging.error(f"❌ Server error: {resp.text[:100]}")
            retry_count += 1
        else:
            logging.warning(f"⚠️ Unexpected status {resp.status_code}: {resp.text[:100]}")
            
    except requests.exceptions.ConnectionError:
        logging.warning("⚠️ API unreachable. Retrying in 10s...")
        time.sleep(10)
        retry_count += 1
        continue
    except Exception as e:
        logging.error(f"⚠️ Unexpected error: {e}")
    
    time.sleep(30)  # Wait 30 seconds between transactions