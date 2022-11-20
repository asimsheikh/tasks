from typing import List, Any
from flask import Flask, render_template, request, redirect, jsonify

from persist import Persist
from models import Task 
from serialize import to_task

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
        print(request.form)
        if request.form['action'] == 'add_task':
            task = Task(name=request.form.get('task_name'))
            db.add(key='tasks', data=task.dict())
            return redirect('/')
        elif request.form['action'] == 'save_task':
            task = to_task(request.form)
            db.update(key='tasks', item_id=task.id, data=task.dict())
            return redirect('/')
    return 'api route'

@app.route('/tasks/<task_id>')
def edit_tasks(task_id: str):
    tasks: List[dict[str, Any]] = [ task for task in db.get('tasks') if task.get('id') == task_id ]
    task = tasks[0]
    if task:
        print(jsonify(task))
        return render_template('edit_task.html', data={'task': task})

    else:
        return jsonify({"ok": False, "error": 'could not find task'})

