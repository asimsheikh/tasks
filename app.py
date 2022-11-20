from typing import List
from flask import Flask, render_template, request, redirect, jsonify

from persist import Persist
from models import Task 

db = Persist()
app = Flask(__name__)

@app.route('/')
def index():
    if db.get_all().get('tasks'):
        return render_template('index.html', data={'tasks': db.get('tasks')})
    else:
        return render_template('index.html', data={'tasks': []})

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        task = Task(name=request.form.get('task_name'))
        db.add(key='tasks', data=task.dict())
        return redirect('/')
    return 'api route'

@app.route('/tasks/<task_id>')
def edit_tasks(task_id: str):
    tasks: List[Task] = [ Task(**task) for task in db.get('tasks') if task.get('id') == task_id ]
    task = tasks[0]
    if task:
        return jsonify(task.dict())
    else:
        return jsonify({"ok": False, "error": 'could not find task'})

