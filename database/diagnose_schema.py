import psycopg2
import os

DB_CONFIG = {
    "dbname": "retail_analytics",
    "user": "analyst",
    "password": "analyst_pass",
    "host": "localhost",
    "port": "5433"  # MUST match docker-compose.yml host port
}

print("🔍 Testing connection...")
try:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()
    print("✅ Connected to PostgreSQL")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("👉 Fix: Check docker-compose.yml ports mapping & credentials")
    exit(1)

sql_path = os.path.join(os.path.dirname(__file__), "schema.sql")
if not os.path.exists(sql_path):
    print(f"❌ schema.sql not found at: {sql_path}")
    exit(1)

with open(sql_path, "r", encoding="utf-8") as f:
    sql = f.read()

print("🛠️ Applying schema statement-by-statement...")
statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
success_count = 0

for i, stmt in enumerate(statements, 1):
    try:
        cur.execute(stmt)
        success_count += 1
    except Exception as e:
        if "already exists" in str(e).lower():
            continue  # Skip if tables already exist
        print(f"❌ Statement {i} failed: {e}")
        print(f" SQL: {stmt[:100]}...")
        cur.close()
        conn.close()
        exit(1)

print(f"✅ Applied {success_count}/{len(statements)} statements")
print("\n📋 Current tables in database:")
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
tables = cur.fetchall()
for t in tables:
    print(f"  • {t[0]}")

cur.close()
conn.close()