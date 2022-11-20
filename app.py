from flask import Flask, render_template, request, redirect

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