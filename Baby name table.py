import os
import re
import psycopg2
from dotenv import load_dotenv

load_dotenv() 
DB_URL = os.getenv("DB_URL")

with open("baby2008.html", "r", encoding="utf-8") as file:
    content = file.read()

matches = re.findall(r"<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>", content)

conn = psycopg2.connect(
    DB_URL,
    sslmode="require",
    keepalives=1,
    keepalives_idle=30,
    keepalives_interval=10,
    keepalives_count=5
)
cur = conn.cursor()
print("Connected successfully to Neon from VS Code!")

cur.execute("""
    CREATE TABLE IF NOT EXISTS babynames (
        id SERIAL PRIMARY KEY,
        rank INT NOT NULL,
        boy_name VARCHAR(100) NOT NULL,
        girl_name VARCHAR(100) NOT NULL
    );
""")

cur.executemany(
    "INSERT INTO babynames (rank, boy_name, girl_name) VALUES (%s, %s, %s);",
    matches
)

conn.commit()
print(f"Successfully saved {len(matches)} rows to Postgres!")


cur.close()
conn.close()
