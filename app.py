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
    global db
    if  request.form.get('action') == 'edit_task':
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
    elif request.form.get('action') == 'add_task':
        task_name: str = request.form.get('task_name') or ''
        db.append(Task(name=task_name))
        form = ''' 
            <div class="m-2" id="add_task">
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_task']"
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="task_name">Add Task</label>
                            <input class="p-2" type="text" value="" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                            <input type="hidden" id="action" name="action" value="add_task">
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
            <div class="m-2" id="tasks" hx-swap-oob="true">
                <p class="text-2xl py-2 font-semibold">Tasks</p>
                {%for task in data.tasks %}
                    {{ task.render() | safe }}
                {% endfor%}
            </div>
        '''
        return render_template_string(form, data={'tasks': db})
    elif request.form.get('action') == 'delete_task':
        task_id = request.form['id']        
        db = [ task for task in db if task.id != task_id]
        return ''
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
            <div class="m-2" id="add_task">
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_task']"
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="task_name">Add Task</label>
                            <input class="p-2" type="text" value="" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                            <input type="hidden" id="action" name="action" value="add_task">
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
            <div class="m-2" id="tasks">
                <p class="text-2xl py-2 font-semibold">Tasks</p>
                {%for task in data.tasks %}
                {{ task.render() | safe }}
                {% endfor%}
            </div>
    '''
    return render_template_string(HEAD + '<body>' + PAGE + '</body>', data={'tasks': db})
