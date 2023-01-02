from flask import Flask, request, render_template_string
from persist import Persist
from models import Task

# db = Persist()
db = [Task(name='Book flights to KL'), Task(name='Acquire Gym Membership')]
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
        <div class="w-1/2">
            <pre class="w-1/2">{{data}}</pre>
        </div>
    '''
    PAGE = '''
            <div>
                {%for task in data.tasks %}
                {{ task.render() | safe }}
                {% endfor%}
            </div>
    '''
    return render_template_string(HEAD + '<body>' + DATA_PAGE + PAGE + '</body>', data={'tasks': db})
