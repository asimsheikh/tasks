from flask import Flask, request, render_template_string
from persist import Persist
from models import Task

from htm import div, p, form, field, button

db = Persist()
app = Flask(__name__)
repo = dict(username='asimsheikh', password='bestintheworld')

HEAD = '''  
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="x-ua-compatible" content="ie=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="{{url_for('static', filename='tailwindcss.min.js')}}"></script>
        <script src="{{url_for('static', filename='htmx.min.js')}}"></script>
    </head>
''' 

@app.route('/testing', defaults={'task_id': None})
@app.route('/testing/<task_id>', methods=['GET','POST', 'PUT'])
def testing(task_id: str):
    if request.method == 'POST' and task_id:
        task = [ task for task in db.get('tasks') if task['id'] == task_id ][0]
        task = Task(**task)
        return f'''
            <form hx-put="/testing/{task.id}" hx-target="div[id='{task.id}']" hx-swap="outerHTML">
                <div>
                    <label class="font-bold">Task Name</label>
                    <input autofocus onfocus="this.select()" class="w-3/4" type="text" name="task_name" value="{task.name}" placeholder="wash the dishes">
                </div>
                <button class="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none">Submit</button>
                <button class="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none" hx-get="/testing/{task.id}">Cancel</button>
            </form> 
        '''

    if request.method == 'GET' and task_id:
        task = [ task for task in db.get('tasks') if task['id'] == task_id ][0]
        task = Task(**task)
        ps = div(
               p(task.name, class_='py-2 text-neutral-500'), 
               p(task.id or '', class_="font-bold text-neutral-700"), 
               class_='p-4 mx-6 my-2 border', id=task.id, hx_post=f'/testing/{task.id}', hx_trigger='dblclick', hx_target=f"div[id='{task.id}']",
               hx_swap='innerHTML'
            )
        return ps

    if request.method == 'PUT' and task_id:
        task = [ task for task in db.get('tasks') if task['id'] == task_id ][0]
        name = request.form['task_name']
        task = Task(**task)
        task.name = name
        db.update('tasks', item_id=task_id,data=task.dict())
        ps = div(
               p(task.name, class_='py-2 text-neutral-500'), 
               p(task.id or '', class_="font-bold text-neutral-700"), 
               class_='p-4 mx-6 my-2 border hover:bg-neutral-200', id=task.id, hx_post=f'/testing/{task.id}', hx_trigger='dblclick', hx_target=f"div[id='{task.id}']",
               hx_swap='innerHTML'
            )
        return ps

    tasks: list[str] = []
    for db_task in db.get('tasks'):
        task = Task(**db_task)
        ps = div(
               p(task.name, class_='py-2 text-neutral-500'), 
               p(task.id or '', class_="font-bold text-neutral-700"), 
               class_='p-4 mx-6 my-2 border hover:bg-neutral-100',
               id=task.id,
               hx_post=f'/testing/{task.id}',
               hx_trigger='dblclick',
               hx_target='this',
               hx_swap=f'#{task.id}'
            )
        tasks.append(ps)
        
    container = div(*tasks, id='pebbles', class_='flex flex-col grow m-2', hx_post='/pebbles', hx_target='#pebbles')
    return render_template_string(HEAD + container, data={})

@app.post('/change/<path:subpath>')
def change(subpath: str):
    if subpath == 'username':
        return render_template_string(''' <!-- html -->
                    <form hx-post="/change/username/add">
                        <input type="text" value="{{data.username}}" name="username" id="username" autofocus onfocus="this.select()"/>
                    </form>
                <!-- !html --> ''', data=repo)
    elif subpath == 'username/add':
        username = request.form['username']
        repo['username'] = username
        page = ''' 
            <div class="border-zinc-700 focus:outline-none"
                id="username"
                hx-post="/change/username"
                hx-trigger="click"
                hx-target="#username"
                hx-swap="outerHTML">Username: {{ data.username }}</div>
        '''
        return render_template_string(HEAD + page, data=repo)
    else:
        return '<div>nothing...</div>'

@app.route('/')
def index():
    page = '''
       <!-- html -->
        <body>
            <div>
              <div class="border-zinc-700 focus:outline-none"
                   id="username"
                   hx-post="/change/username"
                   hx-trigger="click"
                   hx-target="#username"
                   hx-swap="outerHTML">Username: {{ data.username }}</div>

              <div class="border-zinc-700 focus:outline-none"
                   id="password"
                   hx-post="/change"
                   hx-trigger="click"
                   hx-target="#change"
                   hx-swap="outerHTML">Password: {{ data.password }}</div>
            </div>
        </body>
       <!-- !html -->     
    '''
    return render_template_string(HEAD + page, data=repo)