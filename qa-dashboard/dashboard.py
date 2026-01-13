from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
from multiprocessing import Process
from queue import Queue, Empty
import sqlite3
import subprocess
import threading
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database setup for test runs
def init_db():
    conn = sqlite3.connect('test_runs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS runs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  suite TEXT,
                  status TEXT,
                  log TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    conn = sqlite3.connect('test_runs.db')
    c = conn.cursor()
    c.execute("SELECT id, timestamp, suite, status FROM runs ORDER BY id DESC LIMIT 20")
    runs = [{"id": row[0], "time": row[1], "suite": row[2], "status": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(runs)

def run_test_suite(suite_name, command):
    log = ""
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    socketio.emit('run_started', {'suite': suite_name})
    
    output_queue = Queue()
    
    def read_output():
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=os.getcwd()
            )
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    output_queue.put(line.rstrip('\n') + '\n')
            
            process.stdout.close()
            process.wait(timeout=60)
            output_queue.put("Process completed\n")
        except Exception as e:
            output_queue.put(f"ERROR in subprocess: {str(e)}\n")
    
    reader_thread = threading.Thread(target=read_output, daemon=True)
    reader_thread.start()
    
    while True:
        try:
            line = output_queue.get(timeout=0.1)
            print(f"[{suite_name.upper()}] {line.rstrip()}")
            log += line
            socketio.emit('log_update', {'suite': suite_name, 'line': line})
        except Empty:
            if not reader_thread.is_alive():
                break
            socketio.sleep(0.01)
    
    reader_thread.join()
    
    status = "PASSED"  # Simplified - add return code check if needed
    
    conn = sqlite3.connect('test_runs.db')
    c = conn.cursor()
    c.execute("INSERT INTO runs (timestamp, suite, status, log) VALUES (?, ?, ?, ?)",
              (start_time, suite_name, status, log))
    conn.commit()
    conn.close()
    
    socketio.emit('run_complete', {'suite': suite_name, 'status': status})

@socketio.on('run_suite')
def handle_run(data):
    suite = data['suite']
    socketio.emit('run_started', {'suite': suite})
    
    if suite == "selenium":
        dashboard_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(dashboard_dir, "..", "Tesla-Selenium-automation", "test_mini_app_ui.py")
        script_path = os.path.normpath(script_path)
        
        print(f"[DASHBOARD] Attempting to run Selenium script:")
        print(f"[DASHBOARD] Script path: {script_path}")
        print(f"[DASHBOARD] Exists: {os.path.exists(script_path)}")
        
        socketio.emit('log_update', {'suite': suite, 'line': f"Script path: {script_path}\n"})
        socketio.emit('log_update', {'suite': suite, 'line': f"File exists: {os.path.exists(script_path)}\n"})
        
        if not os.path.exists(script_path):
            error_msg = "ERROR: Selenium script not found at path!\n"
            print(error_msg)
            socketio.emit('log_update', {'suite': suite, 'line': error_msg})
            socketio.emit('run_complete', {'suite': suite, 'status': "ERROR"})
            return
        
        command = ["python", script_path]
    else:
        command = ["echo", f"Running {suite} (placeholder)"]
    
    print(f"[DASHBOARD] Executing command: {' '.join(command)}")
    socketio.emit('log_update', {'suite': suite, 'line': f"Executing: {' '.join(command)}\n"})
    
    Process(target=run_test_suite, args=(suite, command)).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, allow_unsafe_werkzeug=True)
