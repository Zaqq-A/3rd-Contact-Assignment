import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv("DB_URL")

conn = psycopg2.connect(DB_URL)
                        
cur = conn.cursor()
print("Connected successfully to Neon from VS Code!")

# CREATE a table
cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name TEXT,
        course TEXT
    );
""")
conn.commit()


# INSERT data

students_data = [
        ("Osimhen", "Python Basics"),
        ("Ronaldo", "Data Analysis"),
        ("Messi", "Web Development"),
        ("Aremu", "Statistical Analysis")
    ]
cur.executemany(
    "INSERT INTO students (name, course) VALUES (%s, %s);",
    students_data
)
conn.commit()

# READ data
cur.execute("SELECT * FROM students;")
print("Current rows:", cur.fetchall())

# UPDATE data
cur.execute(
    "UPDATE students SET course = %s WHERE name = %s;",
    ("Data Science", "Aremu")
)
conn.commit()

# DELETE data
cur.execute("DELETE FROM students WHERE name = %s;",("Aremu",))
conn.commit()

# Clean up
cur.close()
conn.close()
print("All CRUD operations completed!")


