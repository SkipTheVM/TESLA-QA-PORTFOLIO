import sqlite3

conn = sqlite3.connect('todos.db')
c = conn.cursor()

queries = [
    "SELECT * FROM todos;",
    "SELECT COUNT(*) AS total_tasks FROM todos;",
    "SELECT id, task FROM todos ORDER BY id;",
    "SELECT task FROM todos WHERE task LIKE '%tires%';",
    "SELECT * FROM todos WHERE task = '' OR task IS NULL;",
    "SELECT id, task FROM todos ORDER BY id DESC LIMIT 1;"
]

titles = [
    "1. All tasks",
    "2. Total task count",
    "3. Tasks in addition order",
    "4. Tasks containing \"tires\"",
    "5. Empty or null tasks",
    "6. Most recently added task"
]

for i, q in enumerate(queries):
    print("\n" + "="*70)
    print(f" *** {titles[i]} *** ".center(70, "="))
    print("="*70)
    
    c.execute(q)
    rows = c.fetchall()
    if rows:
        # Print headers
        headers = [desc[0] for desc in c.description]
        print(" | ".join(f"{h:<15}" for h in headers))
        print("-"*70)
        # Print rows
        for row in rows:
            print(" | ".join(f"{str(item):<15}" for item in row))
    else:
        print("No results")
    print("="*70)

conn.close()
input("\nDone! Press Enter to exit...")
