from flask import Flask, render_template, request, redirect, url_for, render_template_string
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

@app.route('/users')
def users():
    page = '''
    {% extends "base.html" %}
    {% block content %}
        <div>
        <p><a href={{data.home_url}}>Home</a></p>
        <ul>
            {% for user in data.users %}
            <li>{{user}}</li>
            {% endfor %}
        </ul> 
        </div>
    {% endblock %}
    '''
    users = ['Captain America', 'Ironman', 'Thor', 'Hulk']
    data = {'users': users, 'home_url': url_for('index')}
    return render_template_string(page, data=data)