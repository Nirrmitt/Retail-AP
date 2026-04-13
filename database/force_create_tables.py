import psycopg2
import sys

DB_CONFIG = {
    "dbname": "retail_analytics",
    "user": "analyst",
    "password": "analyst_pass",
    "host": "localhost",
    "port": "5433"  # MUST match your docker-compose.yml host port
}

print("🔌 Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False  # Manual commit required for DDL
    cur = conn.cursor()
    print("✅ Connected successfully.")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("👉 Fix: Ensure Docker is running, DB container is healthy, and port matches docker-compose.yml")
    sys.exit(1)

SQL = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit_cost DECIMAL(10,2) CHECK (unit_cost >= 0),
    unit_price DECIMAL(10,2) CHECK (unit_price >= unit_cost),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(customer_id) ON DELETE CASCADE,
    transaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('completed', 'cancelled', 'refunded')),
    payment_method VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transaction_items (
    item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID REFERENCES transactions(transaction_id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity INTEGER CHECK (quantity > 0),
    unit_price DECIMAL(10,2) CHECK (unit_price >= 0),
    line_total DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

print("🛠️ Executing schema...")
try:
    cur.execute(SQL)
    conn.commit()
    print("✅ Tables created & committed successfully!")
except Exception as e:
    conn.rollback()
    print(f"❌ SQL Execution failed: {e}")
    sys.exit(1)

# Verify immediately
print("\n📋 Verifying tables in database:")
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
tables = cur.fetchall()
for t in tables:
    print(f"  • {t[0]}")

if len(tables) >= 4:
    print("\n🎉 SUCCESS: Database is ready for seeding!")
else:
    print("\n⚠️ Warning: Expected 4 tables, found", len(tables))

cur.close()
conn.close()