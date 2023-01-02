from flask import Flask, request, render_template_string
from persist import Persist

db = Persist()
app = Flask(__name__)

HEAD = '''  
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="x-ua-compatible" content="ie=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="{{url_for('static', filename='tailwindcss.min.js')}}"></script>
        <script src="{{url_for('static', filename='htmx.min.js')}}"></script>
    </head>
''' 

@app.post('/api')
def api():
    return ''

@app.route('/')
def index():
    DATA_PAGE = '''
        <pre>{{data}}</pre>
    '''
    return render_template_string(HEAD + DATA_PAGE, data={})
