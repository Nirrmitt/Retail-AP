import psycopg2
import os

DB_CONFIG = {
    "dbname": "retail_analytics",
    "user": "analyst",
    "password": "analyst_pass",
    "host": "localhost",
    "port": "5433"  # Matches your docker-compose.yml
}

def run_sql_file():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()
    
    sql_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
    
    # Split by semicolon to run multiple statements
    commands = [cmd.strip() for cmd in sql.split(";") if cmd.strip()]
    for cmd in commands:
        try:
            cur.execute(cmd)
        except Exception as e:
            if "already exists" not in str(e):
                print(f"⚠️ Warning: {e}")
    
    print("✅ Schema applied successfully")
    cur.close()
    conn.close()

if __name__ == "__main__":
    run_sql_file()