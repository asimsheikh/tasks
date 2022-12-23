from flask import Flask, request, render_template, render_template_string
from persist import Persist
from models import Task

from html import div, p

db = Persist()
app = Flask(__name__)

@app.route('/clear')
def temp_clear():
	db.clear()
	return 'Cleared'

@app.route('/testing', methods=['GET','POST'])
def testing():
	if request.method == 'POST':
		return '<h1>Asim</h1>'

	tasks: list[str] = []
	for db_task in db.get('tasks'):
		task = Task(**db_task)
		ps = div(
			   p(task.name, class_='py-2 text-neutral-500'), 
			   p(task.id, class_="font-bold text-neutral-700"), 
			   class_='p-4 mx-6 my-2 border hover:border-4'
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
