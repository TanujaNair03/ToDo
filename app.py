from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime

# --- Initialization ---
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable Cross-Origin Resource Sharing

DATA_FILE = "tasks.json"

# --- Helper Functions ---
def load_tasks():
    """Loads tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_tasks(tasks):
    """Saves tasks to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# --- API Endpoints ---
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Endpoint to get all tasks."""
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Endpoint to add a new task."""
    new_task_data = request.json
    tasks = load_tasks()
    date_str = new_task_data['date']

    if date_str not in tasks:
        tasks[date_str] = []

    task_to_add = {'task': new_task_data['task'], 'done': False}
    tasks[date_str].append(task_to_add)
    save_tasks(tasks)
    return jsonify({"message": "Task added successfully"}), 201

@app.route('/api/tasks/update', methods=['PUT'])
def update_task():
    """Endpoint to update a task's status."""
    update_data = request.json
    tasks = load_tasks()
    
    date_str = update_data['date']
    task_index = update_data['taskIndex']
    new_status = update_data['done']

    if date_str in tasks and 0 <= task_index < len(tasks[date_str]):
        tasks[date_str][task_index]['done'] = new_status
        save_tasks(tasks)
        return jsonify({"message": "Task updated successfully"})
    
    return jsonify({"message": "Task not found"}), 404

@app.route('/api/tasks/edit', methods=['PUT'])
def edit_task():
    """Endpoint to edit a task's description."""
    edit_data = request.json
    tasks = load_tasks()
    
    date_str = edit_data['date']
    task_index = edit_data['taskIndex']
    new_text = edit_data['newTaskText']

    if date_str in tasks and 0 <= task_index < len(tasks[date_str]):
        tasks[date_str][task_index]['task'] = new_text
        save_tasks(tasks)
        return jsonify({"message": "Task edited successfully"})
    
    return jsonify({"message": "Task not found"}), 404

@app.route('/api/tasks/<string:date>/<int:task_index>', methods=['DELETE'])
def delete_task(date, task_index):
    """Endpoint to delete a task."""
    tasks = load_tasks()

    if date in tasks and 0 <= task_index < len(tasks[date]):
        # Remove the task from the list
        tasks[date].pop(task_index)
        # If the day has no more tasks, remove the date entry entirely
        if not tasks[date]:
            del tasks[date]
        save_tasks(tasks)
        return jsonify({"message": "Task deleted successfully"})
    
    return jsonify({"message": "Task not found"}), 404

# --- Serve Frontend ---
@app.route('/')
def serve_index():
    """Serves the main index.html file."""
    return send_from_directory(app.static_folder, 'index.html')

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)