from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
## Creates database and table if they don't already exist
def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT, done INTEGER)''')
    conn.commit()
    conn.close()
init_db()

## Home Page - serves the HTML UI
@app.route('/')
def index():
    return render_template('index.html')

## API: Get all todo's
@app.route('/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM todos")
    rows = c.fetchall()
    conn.close

    todos = []
    for row in rows:
        todos.append({
            "id": row[0],
            "task": row[1],
            "done":bool(row[2])
            })
    return jsonify(todos)
        

## API: Add a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    task = data.get('task')
    if not task:
        return jsonify({"error": "task required"}), 400
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute("INSERT INTO todos (task, done) VALUES (?, 0)", (data['task'],))
    conn.commit()
    conn.close()
    return jsonify({"status": "added"}), 201
  
if __name__ == '__main__':
    app.run(debug=False)

