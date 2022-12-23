from flask import Flask, request, render_template, render_template_string
from persist import Persist
from models import Task

from htm import div, p

db = Persist()
app = Flask(__name__)

@app.route('/clear')
def temp_clear():
	db.clear()
	return 'Cleared'

@app.route('/testing', defaults={'task_id': None})
@app.route('/testing/<task_id>', methods=['GET','POST', 'PUT'])
def testing(task_id: str):
	if request.method == 'POST' and task_id:
		task = [ task for task in db.get('tasks') if task['id'] == task_id ][0]
		task = Task(**task)
		return f'''
			<form hx-put="/testing/{task.id}" hx-target="div[id='{task.id}']" hx-swap="outerHTML">
				<div>
					<label>Task Name</label>
					<input class="w-full" type="text" name="task_name" value="{task.name}" placeholder="wash the dishes">
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
			   class_='p-4 mx-6 my-2 border',
			   id=task.id,
			   hx_post=f'/testing/{task.id}',
			   hx_trigger='dblclick',
			   hx_target=f"div[id='{task.id}']",
			   hx_swap='innerHTML'
			)
		return ps

	if request.method == 'PUT' and task_id:
		task = [ task for task in db.get('tasks') if task['id'] == task_id ][0]
		task = Task(**task)
		ps = div(
			   p(task.name, class_='py-2 text-neutral-500'), 
			   p(task.id or '', class_="font-bold text-neutral-700"), 
			   class_='p-4 mx-6 my-2 border',
			   id=task.id,
			   hx_post=f'/testing/{task.id}',
			   hx_trigger='dblclick',
			   hx_target=f"div[id='{task.id}']",
			   hx_swap='innerHTML'
			)
		return ps


	tasks: list[str] = []
	for db_task in db.get('tasks'):
		task = Task(**db_task)
		ps = div(
			   p(task.name, class_='py-2 text-neutral-500'), 
			   p(task.id or '', class_="font-bold text-neutral-700"), 
			   class_='p-4 mx-6 my-2 border',
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
