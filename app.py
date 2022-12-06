from typing import List, Any
from flask import Flask, render_template, request, redirect, jsonify, url_for
from jinja2 import Template

from persist import Persist
from models import Task
from serialize import to_task, to_note

db = Persist()
app = Flask(__name__)

@app.route('/clear')
def temp_clear():
    db.clear()
    return 'Cleared'

@app.route('/')
def index():
    if db.get_all().get('tasks'):
        return render_template('index.html', data={'tasks': db.get('tasks')})
    else:
        return render_template('index.html', data={'tasks': []})

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        if request.form['action'] == 'add_task':
            task = Task(name=request.form.get('task_name'))
            db.add(key='tasks', data=task.dict())
            return redirect('/')
        elif request.form['action'] == 'save_task':
            task = to_task(request.form)
            db.update(key='tasks', item_id=task.id, data=task.dict())
            return redirect('/')
        elif request.form['action'] == 'add_notes':
            note = to_note(request.form)
            db.add(key='notes', data=note.dict())
            return redirect('/notes/' + request.form['notes_task_id'])
        elif request.form['action'] == 'save_note':
            note = to_note(request.form)
            db.update(key='notes', item_id=note.id, data=note.dict())
            return redirect('/notes/' + request.form['notes_task_id'])
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

@app.route('/notes/<task_id>')
def edit_notes(task_id: str):
    tasks: List[dict[str, Any]] = [ task for task in db.get('tasks') if task.get('id') == task_id ]
    notes: List[dict[str, Any]] = [ note for note in db.get('notes') if note.get('task_id') == task_id ]
    print(notes)
    task = tasks[0]
    if task:
        return render_template('edit_notes.html', data={'task': task, 'notes': notes})
    else:
        return jsonify({"ok": False, "error": 'could not find task'})

@app.route('/tasks/delete/<task_id>')
def delete_task(task_id: str):
    print(task_id)
    db.delete(key='tasks', item_id=task_id)
    return redirect('/')

@app.route('/edit/<path:subpath>')
def path(subpath: str):
    entity, entity_id = subpath.split('/')
    if entity == 'notes':
        note: dict[str, Any] = [note for note in db.get('notes') if note.get('id') == entity_id][0]
        return render_template('edit_note.html', data={'note': note })
    return subpath 

@app.route('/users')
def users():
    page = '''
    {% extends "base.html" %}
     <div>
      <p><a href={{data.home_url}}>Home</a></p>
       <ul>
         {% for user in data.users %}
           <li>{{user}}</li>
         {% endfor %}
       </ul> 
     </div>
    '''
    users = ['Captain America', 'Ironman', 'Thor', 'Hulk']
    return Template(page).render(data={'users': users, 'home_url': url_for('index')})