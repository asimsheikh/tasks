from flask import Flask, request, render_template_string

from persist import Persist

db = Persist()
app = Flask(__name__)

@app.route('/clear')
def temp_clear():
    db.clear()
    return 'Cleared'

@app.route('/pebble',  methods=['POST'])
def pebble():
	print(request.form)
	data = dict(pebble_id=int(request.form['pebble_id']), id=request.form['id'])
	page='''
        <div id="{{ data.pebble_id }}" class="grow mx-2 bg-red-300 w-14"
            hx-post="/pebble" hx-swap="outerHTML" 
            hx-vals='{"pebble_id": {{ data.pebble_id}}, "id": "{{ data.id }}" }'>
            {{ data.pebble_id }} {{ data.id }} 
        </div>
	'''
	return render_template_string(page, data=data)

@app.route('/')
def index():
    page = '''
    {% extends "base.html" %}
    {% block content %}
        <div class="mb-4">
          <p class="text-xl font-extrabold">Pebbles App</p>
        </div>
        <div id="pebbles" class="flex flex-row">
          {% for pebble in data.pebbles %}
            <div id="{{ pebble.pebble_id }}" class="grow mx-2 bg-green-300 w-14"
                hx-post="/pebble" hx-swap="outerHTML" 
                hx-vals='{"pebble_id": {{ pebble.pebble_id}}, "id": "{{ pebble.id }}" }'>
                {{ pebble.pebble_id }} 
            </div>
          {% endfor %}
        <div>
    {% endblock %}
    '''
    pebbles = db.get('pebbles')
    return render_template_string(page, data={"pebbles": pebbles})
