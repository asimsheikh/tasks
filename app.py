from flask import Flask, request, render_template, render_template_string
from persist import Persist
from models import Task

from htm import div, p
from temp import form, field, button

db = Persist()
app = Flask(__name__)

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
    head = '''  
        <head>
            <meta charset="utf-8" />
            <meta http-equiv="x-ua-compatible" content="ie=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <script src="{{url_for('static', filename='tailwindcss.min.js')}}"></script>
            <script src="{{url_for('static', filename='htmx.min.js')}}"></script>
        </head>
    ''' 
    return render_template_string(head + container, data={})

@app.route('/pebble',  methods=['POST'])
def pebble():
    pebble = [ pebble for pebble in db.get('pebbles') if pebble['id'] == request.form['id'] ][0]
    pebble = { **pebble,**{"checked": not pebble['checked']}}
    db.update('pebbles', request.form['id'], pebble)
    pebbles = db.get('pebbles')
    pebbles = [pebbles[i:i+4] for i in range(0, 96, 4)]
    return render_template('pebbles.html', data={"pebbles": pebbles})

@app.route('/')
def index():
    pebbles = db.get('pebbles')
    pebbles = [pebbles[i:i+4] for i in range(0, 96, 4)]
    return render_template('pebbles.html', data={"pebbles": pebbles})

@app.route('/forms', methods=['GET', 'POST'])
def forms():
    if request.method == 'POST':
        print(request.form)
        task_name = request.form['task_name']
        task_date = request.form['task_date']
        return div(
                p(task_name, class_='py-2 text-neutral-500'), 
                p(task_date, class_='py-2 text-neutral-500'), 
                p(request.form['task_allocation'], class_="font-bold text-neutral-700"), 
                class_='p-4 mx-6 my-2 border')

    template = form(
                field(label='Task Name', id='task_name', name='task_name', type='text', value='First task', autofocus=True), 
                field(label='Task Allocation', id='task_allocation', name='task_allocation', type='text', value="projects"),
                field(label='Date', id='task_date', name='task_date', type='date', value="2022-12-25"),
                button(class_="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none", text='Submit', onclick='submit'),
                button(class_="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none",text='Cancel', onclick=''),
                post='/forms')
    head = '''  
        <head>
            <meta charset="utf-8" />
            <meta http-equiv="x-ua-compatible" content="ie=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <script src="{{url_for('static', filename='tailwindcss.min.js')}}"></script>
            <script src="{{url_for('static', filename='htmx.min.js')}}"></script>
        </head>
    ''' 
    return render_template_string(head + template)

@app.route('/htmx/', defaults={'id': None})
@app.route('/htmx/<id>', methods=('GET', 'POST'))
def htmx_test(id: str):
    if id and request.method=='POST':
        return div(
                p(id, class_='text-neutral-200'),
               id=id, hx_post=f'/htmx/{id}', hx_trigger='dblclick',
               hx_target='this', hx_swap='outerHTML', class_='p-10 bg-blue-400 border-2')

    head = '''  
        <head>
            <meta charset="utf-8" />
            <meta http-equiv="x-ua-compatible" content="ie=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <script src="{{url_for('static', filename='tailwindcss.min.js')}}"></script>
            <script src="{{url_for('static', filename='htmx.min.js')}}"></script>
        </head>
    ''' 
    divs = div(
              div(
                div(
                    p('The next element', class_='text-neutral-200'), 
                id='1', hx_post='/htmx/1', hx_trigger='dblclick', hx_target='this', hx_swap='outerHTML', class_='p-10 bg-red-200'),

                div(
                    p('The next element', class_='text-neutral-200'),
                    id='2', hx_post='/htmx/2', hx_trigger='dblclick', hx_target='this', hx_swap='outerHTML', class_='p-10 bg-red-300'),

                div(
                    p('The next element', class_='text-neutral-200'),
                    id='3', hx_post='/htmx/3', hx_trigger='dblclick', hx_target='5', hx_swap='outerHTML', class_='p-10 bg-red-400'),

                id='container', class_='p-10 bg-neutral-800 flex'),
            
                div(
                    p('The swapped element position', class_='p-10 font-bold text-2xl text-neutral-200'),
                    id='5', class_='p-10 bg-neutral-800 flex',
                ), 
            ) 

    return render_template_string(head + divs)