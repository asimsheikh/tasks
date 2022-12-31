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
        <!-- html -->
        
            <div class="border-zinc-700 focus:outline-none"
                id="username"
                hx-post="/change/username"
                hx-trigger="click"
                hx-target="#username"
                hx-swap="outerHTML">Username: {{ data.username }}</div>

        <!-- !html -->     
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