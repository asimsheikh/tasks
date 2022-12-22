from flask import Flask, request, render_template
from persist import Persist

db = Persist()
app = Flask(__name__)

@app.route('/clear')
def temp_clear():
	db.clear()
	return 'Cleared'

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
