from flask import Flask, request, render_template_string
from persist import Persist
from models import Task

# db = Persist()
db = [Task(name='Book flights to KL'),
      Task(name='Acquire Gym Membership'),
      Task(name='Establish a lease in BKK'),]

app = Flask(__name__)

HEAD = '''  
<!-- html -->
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="x-ua-compatible" content="ie=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="{{url_for('static', filename='tailwindcss.min.js')}}"></script>
        <script src="{{url_for('static', filename='htmx.min.js')}}"></script>
    </head>
<!-- !html -->
''' 

@app.post('/api')
def api():
    print(request.form)
    if not request.form.get('action'):
        task_id = request.form['id']
        task = [task for task in db if task.id == task_id][0]
        return render_template_string(task.edit())
    elif request.form.get('action') == 'update_task':
        task_id = request.form['id']
        task_name = request.form['task_name']
        for task in db:
            if task.id == task_id:
               task.name = task_name
               return render_template_string(task.render())
        raise TypeError
    else:
        raise TypeError

@app.route('/')
def index():
    DATA_PAGE = '''
    <!-- html -->
        <div class="w-1/2">
            <pre class="w-1/2">{{data}}</pre>
        </div>
    <!-- !html -->
    '''
    PAGE = '''
            <div class="m-2">
                <p class="text-2xl py-2 font-semibold">Tasks</p>
                {%for task in data.tasks %}
                {{ task.render() | safe }}
                {% endfor%}
            </div>
    '''
    return render_template_string(HEAD + '<body>' + PAGE + '</body>', data={'tasks': db})
