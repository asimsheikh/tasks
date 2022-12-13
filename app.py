from flask import Flask, request, redirect, render_template_string

from persist import Persist
from models import Task

db = Persist()
app = Flask(__name__)

@app.route('/clear')
def temp_clear():
    db.clear()
    return 'Cleared'

@app.route('/')
def index():
    page = '''
    {% extends "base.html" %}
    {% block content %}
        <div>
            <p><a class="font-extrabold pb-2" href={{url_for('index')}}>Home</a></p>
            <p>In the tasks app</p>
        </div>
    {% endblock %}
    '''
    return render_template_string(page, data={})

@app.route('/api/<entity>', methods=['POST', 'GET'])
def api(entity: str):
    if request.method == 'GET':
        page = '''
        {% extends "base.html" %}
        {% block content %}
            <form hx-post="/api/tasks">
            <pre class='text-gray-400 pl-40'>{{data | pprint}}</pre>
                <div class='my-4'>
                    <input class="text-neutral-800" type="text" name="task_name" value="">
                </div>
                <div>
                    <button class="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none">Add Task</button>
                </div>
                <input type="hidden" name="action" value="add_task" />
                <input type="hidden" name="user" value="asimsheikh" />
                <div>
                    <p><a class="font-extrabold pb-2" href={{url_for('index')}}>Home</a></p>
                    {% for task in data.tasks %}
                        <p>{{task.name}}</p>
                    {% endfor %}
                </div>
            </form>
        {% endblock %}
        '''
        db_all = db.get_all()
        data = {'tasks': db_all.get('tasks', [])}
        return render_template_string(page, data=data)

    elif request.method == 'POST' and request.headers['HX-Request'] and request.form.get('action') == "add_task":
        print(request.headers)
        print(request.form)
        task = Task(name=request.form.get('task_name', ''))
        db.add('tasks', data=task.dict())
        page = '''
        {% extends "base.html" %}
        {% block content %}
            <form hx-post="/api/tasks">
            <pre class='text-gray-400 pl-40'>{{data | pprint}}</pre>
                <div class='my-4'>
                    <input class="text-neutral-800" type="text" name="task_name" value="">
                </div>
                <div>
                    <button class="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none">Add Task</button>
                </div>
                <input type="hidden" name="action" value="add_task" />
                <div>
                    <p><a class="font-extrabold pb-2" href={{url_for('index')}}>Home</a></p>
                    {% for task in data.tasks %}
                        <p>{{task.name}}</p>
                    {% endfor %}
                </div>
            </form>
        {% endblock %}
        '''

        db_all = db.get_all()
        data = {'tasks': db_all.get('tasks', [])}
        return render_template_string(page, data=data)
    
    elif request.method == 'POST' and entity == "tasks":
        print(request.form)
        return redirect('/')

    return 'In api routes'

@app.route('/contacts/<string:id>', methods=['GET', 'POST', 'PUT'])
def contacts(id: str):
    if request.method == 'POST':
        page = ''' 
            <form hx-put="/contacts/{{ data.contact.id }}" hx-target="this" hx-swap="outerHTML">
                <pre class='text-gray-400 pl-40'>{{data | pprint}}</pre>
                <div>
                    <label>First Name</label>
                    <input class="text-neutral-800" type="text" name="contact_first_name" value="{{ data.contact.first_name }}">
                </div>
                <div>
                    <label>Last Name</label>
                    <input class="text-neutral-800" type="text" name="contact_last_name" value="{{ data.contact.last_name }}">
                </div>
                <div>
                    <label>Email Address</label>
                    <input class="text-neutral-800" type="email" name="contact_email" value="{{ data.contact.email }}">
                    <input type="hidden" name="contact_id" value="{{ data.contact.id }}">
                </div>
                <button class="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none">Submit</button>
                <button class="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none" hx-get="/contacts/{{ data.contact.id }} ">Cancel</button>
            </form> 
        '''
        contacts = db.get(key='contacts')
        data = {'contact': contacts[0]}
        return render_template_string(page, data=data)

    elif request.method == 'PUT':
        contact = to_contact(request.form)
        db.update('contacts', contact.id, data=contact.dict())

    page = '''
    {% extends "base.html" %}
    {% block content %}
        <div hx-target="this" hx-swap="outerHTML">
        <pre class='text-gray-400 pl-40'>{{data | pprint}}</pre>
            <label>First Name</label> {{ data.contact.first_name}}<br/>
            <label>Last Name</label> {{ data.contact.last_name }}<br/>
            <label>Email</label> {{ data.contact.email }} <br/>
            <button hx-post="/contacts/{{ data.contact.id }}" class="rounded-md mt-2 border-2 border-zinc-700 p-2 focus:outline-none" > Click To Edit </button>
        </div>
    {% endblock %}
    '''
    contacts = db.get(key='contacts')
    data = {'contact': contacts[0]}
    return render_template_string(page, data=data)
