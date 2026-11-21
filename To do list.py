import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")

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
    CREATE TABLE IF NOT EXISTS todolist (
        id SERIAL PRIMARY KEY,
        task TEXT NOT NULL,
        is_done BOOLEAN DEFAULT FALSE
    );
""")
conn.commit()


def add_task():
    task = input("Enter a new task: ").strip()
    if task:
        cur.execute("INSERT INTO todolist (task) VALUES (%s);", (task,))
        conn.commit()
        print("Task added!")

def view_tasks():
    cur.execute("SELECT id, task, is_done FROM todolist ORDER BY id;")
    rows = cur.fetchall()
    print("\n--- YOUR TO-DO LIST ---")
    if not rows:
        print("No tasks yet.")
    for task_id, task, is_done in rows:
        status = "[x]" if is_done else "[ ]"
        print(f"{task_id}. {status} {task}")
    print("-----------------------\n")

def mark_done():
    view_tasks()
    task_id = input("Enter the ID of the task to mark as done: ").strip()
    cur.execute("UPDATE todolist SET is_done = TRUE WHERE id = %s;", (task_id,))
    conn.commit()
    print("Task updated!")

def delete_task():
    view_tasks()
    task_id = input("Enter the ID of the task to delete: ").strip()
    cur.execute("DELETE FROM todolist WHERE id = %s;", (task_id,))
    conn.commit()
    print("Task deleted!")

# Main interactive menu loop
while True:
    print("1. Add Task | 2. View Tasks | 3. Mark Done | 4. Delete Task | 5. Exit")
    choice = input("Choose an option (1-5): ").strip()

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1-5.")

# Clean up connection on exit
cur.close()
conn.close()
